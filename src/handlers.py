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
from src.actions import create_search

Base.metadata.create_all(bind=engine)

app = FastAPI()

bookings = []


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_response_a(loop: asyncio.AbstractEventLoop, booking_id: int, db: Session):
    future = loop.run_in_executor(None, requests.post, f'http://127.0.0.1:9001/search/{booking_id}/')
    req = await future
    booking = req.json()

    await insert_data(db, booking, booking_id)


async def get_response_b(loop: asyncio.AbstractEventLoop, booking_id: int, db: Session):
    future = loop.run_in_executor(None, requests.post, f'http://127.0.0.1:9002/search/{booking_id}/')
    req = await future
    booking = req.json()

    await insert_data(db, booking, booking_id)


@app.post('/search/{booking_id_a}/{booking_id_b}')
async def search(booking_id_a: int, booking_id_b: int, db: Session = Depends(get_db)):
    loop = asyncio.get_event_loop()
    await create_search(db, {'id': uuid.uuid4(),
                             'status': 'PENDING',
                             'booking_ids': ''})
    await asyncio.gather(get_response_a(loop, booking_id_a, db),
                         get_response_b(loop, booking_id_b, db))


# @app.get('/results/{search_id}/{currency}')
# async def search(search_id: uuid.uuid4, currency: str):
#     res = await get_data(db, booking_id)
#     await asyncio.sleep(30)
#     return res
#     pass


@app.get('/currency')
async def currency():
    request = requests.get('https://www.nationalbank.kz/rss/get_rates.cfm?fdate=26.10.2021')
    data = request.json()
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)
