from fastapi import APIRouter, HTTPException
from web3_client.client import client


router = APIRouter()


@router.get('/token_info')
async def get_token_info():
    return client.get_token_info()


@router.get('/balance/')
async def get_balance(address: str):
    balance = client.get_balance(address)
    return {'balance': balance}


@router.post('/get_balances/')
async def get_balances(addresses: list[str]):
    try:
        balances = client.get_balances(addresses)
        return {'balances': balances}
    except HTTPException as e:
        return HTTPException(status_code=500, detail=str(e))


@router.get('/top_balances')
async def get_top_balances(limit: int = 3):
    return await client.get_top_balances(limit)


@router.get('/top_balances_with_transactions')
async def get_top_balances_with_transactions(limit: int = 3, balance_with_transactions: bool = False):
    return await client.get_top_balances(limit, balance_with_transactions)
