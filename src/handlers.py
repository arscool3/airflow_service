import asyncio
import uuid

import uvicorn
import requests
import xmltodict
from decimal import Decimal

from fastapi import FastAPI
from sqlalchemy.orm import Session

from src.models import Search, Currency
from src.database import database
from src.tools import insert_data
from src.actions import create_search, create_currency, get_search, create_segment, update_search

app = FastAPI()

bookings = []


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


async def get_response_a(loop: asyncio.AbstractEventLoop, booking_id: int, search_id: uuid.uuid4, db: Session):
    future = loop.run_in_executor(None, requests.post, f'http://127.0.0.1:9001/search/{booking_id}/')
    req = await future
    booking = req.json()

    await insert_data(db, booking, search_id)


async def get_response_b(loop: asyncio.AbstractEventLoop, booking_id: int, search_id: uuid.uuid4, db: Session):
    future = loop.run_in_executor(None, requests.post, f'http://127.0.0.1:9002/search/{booking_id}/')
    req = await future
    booking = req.json()

    await insert_data(db, booking, search_id)


@app.post('/search/{booking_id_a}/{booking_id_b}')
async def search(booking_id_a: int, booking_id_b: int):
    loop = asyncio.get_event_loop()
    search = Search(uuid.uuid4(), 'PENDING')
    await create_search(database, search)
    await asyncio.gather(get_response_a(loop, booking_id_a, search.id, database),
                         get_response_b(loop, booking_id_b, search.id, database))
    await update_search(database, search.id)
    return search.id


@app.get('/results/{search_id}/{currency}')
async def get_results(search_id: str, currency: str):
    future = asyncio.Future()
    await get_search(future, database, search_id, currency)
    result = await future
    return result


@app.post('/currency')
async def currency():
    request = requests.get('https://www.nationalbank.kz/rss/get_rates.cfm?fdate=26.10.2021')
    data = xmltodict.parse(request.text)
    await create_currency(database, Currency('KZT', Decimal(1)))
    for currency in data['rates']['item']:
        ins_currency = Currency(currency['title'], currency['description'])
        await create_currency(database, ins_currency)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)
