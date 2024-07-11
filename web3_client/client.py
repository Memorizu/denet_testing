import requests
from web3 import Web3

from config import settings
from web3_client.erc20_abi import abi


class Client:
    def __init__(self, provider_url, contract_address, abi):
        self.web3 = Web3(Web3.HTTPProvider(provider_url))

        self.contract_address =  Web3.to_checksum_address(contract_address)
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=abi)
        self.api_key = settings.w3.api_key

    def get_name(self):
        return self.contract.functions.name().call()

    def get_symbol(self):
        return self.contract.functions.symbol().call()

    def get_total_supply(self):
        return self.contract.functions.totalSupply().call()

    def get_balance(self):
        addr = Web3.to_checksum_address(self.contract_address)
        balance = self.contract.functions.balanceOf(addr).call()
        decimals = self.contract.functions.decimals().call()
        return balance / (10 ** decimals)

    def get_balances(self, addresses):
        balances = []
        for address in addresses:
            balances.append(self.get_balance(address))
        return balances

    def get_top_balances(self, n):
        url = f"https://api.polygonscan.com/api"
        params = {
            'module': 'account',
            'action': 'tokentx',
            'contractaddress': self.contract_address,
            'page': 1,
            'offset': 10000,
            'sort': 'desc',
            'apikey': self.api_key
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data['status'] != '1':
            raise Exception("Error fetching data from Polygonscan")

        balances = {}
        for tx in data['result']:
            to = tx['to']
            value = int(tx['value'])
            if to in balances:
                balances[to] += value
            else:
                balances[to] = value

        sorted_balances = sorted(balances.items(), key=lambda x: x[1], reverse=True)
        return sorted_balances[:n]

    def get_top_balances_with_transactions(self, n):
        pass

    def get_token_info(self):
        return {
            "symbol": self.get_symbol(),
            "name": self.get_name(),
            "totalSupply": self.get_total_supply()
        }


client = Client(
    provider_url=settings.w3.provider_url,
    contract_address=settings.w3.token_address,
    abi=abi
)
