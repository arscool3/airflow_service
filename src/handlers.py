import asyncio
import json
from pprint import pprint

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


@app.post('/insert_data')
async def search(db: Session = Depends(get_db)):
    file = open('src/data/response_a.json')
    json_data = json.load(file)
    booking_list = list(json_data)

    await insert_data(db, booking_list)


@app.post('/search')
async def search(db: Session = Depends(get_db)):
    await task(db)
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(task(db)),
             loop.create_task(print())]
    wait_tasks = asyncio.wait(tasks)
    loop.run_until_complete(wait_tasks)
    loop.close()


async def print():
    pprint(len(bookings))
    return len(bookings)


@app.post('/task')
async def task(db: Session = Depends(get_db)):
    _id = 0
    _id += 1
    res = await get_data(db, _id)
    bookings.append(res)
    await asyncio.sleep(1)
