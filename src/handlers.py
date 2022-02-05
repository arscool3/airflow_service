import asyncio
import json
import uvicorn
import requests

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from src.database import SessionLocal, engine
from src.models import Base
from src.tools import insert_data, get_data

Base.metadata.create_all(bind=engine)

app = FastAPI()

bookings = []


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_response_a(start_date: int, end_date: int, db: Session):
    req = requests.post(f'http://127.0.0.1:9001/search/from/{start_date}/to/{end_date}/')
    json_data = req.json()
    booking_list = list(json_data)

    await insert_data(db, booking_list)


async def get_response_b(start_date: int, end_date: int, db: Session):
    req = requests.post(f'http://127.0.0.1:9002/search/from/{start_date}/to/{end_date}/')
    json_data = req.json()
    booking_list = list(json_data)

    await insert_data(db, booking_list)


async def get_responses(start_date: int, end_date: int, db: Session):
    await get_response_a(start_date, end_date, db)
    await get_response_b(start_date, end_date, db)


@app.post('/search/from/{start_date}/end/{end_date}')
async def search(start_date: int, end_date: int, db: Session = Depends(get_db)):
    await get_responses(start_date, end_date, db)


@app.post('/search/{booking_id}')
async def search(booking_id: int, db: Session = Depends(get_db)):
    res = await get_data(db, booking_id)
    await asyncio.sleep(30)
    return res


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
