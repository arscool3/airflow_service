import asyncio
import json
import uuid

import uvicorn
import requests
import xmltodict

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from src.database import SessionLocal, engine
from src.models import Base, Search
from src.tools import insert_data, get_data
from src.actions import create_search, create_currency, get_search, create_segment, update_search

Base.metadata.create_all(bind=engine)

app = FastAPI()

bookings = []


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
async def search(booking_id_a: int, booking_id_b: int, db: Session = Depends(get_db)):
    loop = asyncio.get_event_loop()
    search_id = uuid.uuid4()
    await create_search(db, {'id': search_id,
                             'status': 'PENDING'})
    await asyncio.gather(get_response_a(loop, booking_id_a, search_id, db),
                         get_response_b(loop, booking_id_b, search_id, db))
    await update_search(db, search_id)
    return search_id


@app.post('/results/{search_id}/{currency}')
async def get_results(search_id: str, currency: str, db: Session = Depends(get_db)):
    future = asyncio.Future()
    await get_search(future, db, search_id)
    result = await future
    return result


@app.post('/currency')
async def currency(db: Session = Depends(get_db)):
    request = requests.get('https://www.nationalbank.kz/rss/get_rates.cfm?fdate=26.10.2021')
    data = xmltodict.parse(request.text)
    for currency in data['rates']['item']:
        await create_currency(db, {'title': currency['title'],
                                   'amount': currency['description']})


@app.post('/seg')
async def create_seg(db: Session = Depends(get_db)):
    future = asyncio.Future()
    segment = {'operating_airline': 'operating_airline',
               'marketing_airline': 'marketing_airline',
               'flight_number': 123,
               'equipment': 'equipment',
               'baggage': 'baggage',
               'dep_airport': 'dep',
               'arr_airport': 'arr'}
    await create_segment(future, db, segment)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)

