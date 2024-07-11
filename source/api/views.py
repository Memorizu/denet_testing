from fastapi import APIRouter, Depends
from web3_client.client import Client, client


router = APIRouter()


@router.get('/balance')
async def get_balance():
    balance = client.get_balance()
    return {'balance': balance}


@router.get('/symbol')
async def get_symbol():
    symbol = client.get_symbol()
    return {'symbol': symbol}


@router.get('/total_supply')
async def get_total_supply():
    total_supply = client.get_total_supply()
    return {'total_supply': total_supply}
