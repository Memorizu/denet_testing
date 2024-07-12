import requests
from web3 import Web3
import httpx
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

    def get_balance(self, address):
        address = Web3.to_checksum_address(address)
        balance = self.contract.functions.balanceOf(address).call()
        return balance

    def get_balances(self, addresses):
        balances = []
        for address in addresses:
            balances.append(self.get_balance(address))
        return balances

    async def get_top_balances(self, limit:int = 3, balance_with_transaction=False):
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

        async with httpx.AsyncClient() as async_client:
            response = await async_client.get(url, params=params)
            data = response.json()

        if data['status'] != '1':
            raise Exception("Error fetching data from Polygonscan")

        balances = {}
        transactions = {}
        for tx in data['result']:
            to = tx['to']
            value = int(tx['value'])
            if to in balances:
                balances[to] += value
            else:
                balances[to] = value

            if balance_with_transaction:
                timestamp = int(tx['timeStamp'])
                if to in transactions:
                    if transactions[to] < timestamp:
                        transactions[to] = timestamp
                else:
                    transactions[to] = timestamp

        sorted_balances = sorted(balances.items(), key=lambda x: x[1], reverse=True)
        top_balances = sorted_balances[:limit]

        if balance_with_transaction:
            return [(address, balance / (10 ** self.contract.functions.decimals().call()), transactions[address])
                    for address, balance in top_balances]

        return [(address, balance / (10 ** self.contract.functions.decimals().call())) for address, balance in top_balances]

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
