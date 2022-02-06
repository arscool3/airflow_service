import asyncio
import uuid

import uvicorn
import requests
import xmltodict

from fastapi import FastAPI
from sqlalchemy.orm import Session

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
    search_id = uuid.uuid4()
    await create_search(database, {'id': search_id,
                                   'status': 'PENDING'})
    await asyncio.gather(get_response_a(loop, booking_id_a, search_id, database),
                         get_response_b(loop, booking_id_b, search_id, database))
    await update_search(database, search_id)
    return search_id


@app.post('/results/{search_id}/{currency}')
async def get_results(search_id: str, currency: str):
    future = asyncio.Future()
    await get_search(future, database, search_id)
    result = await future
    return result


@app.post('/currency')
async def currency():
    request = requests.get('https://www.nationalbank.kz/rss/get_rates.cfm?fdate=26.10.2021')
    data = xmltodict.parse(request.text)
    for currency in data['rates']['item']:
        await create_currency(database, {'title': currency['title'],
                                         'amount': currency['description']})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)
