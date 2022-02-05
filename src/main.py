import json

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from src.crud import create_flight, create_booking, create_segment
from src.database import SessionLocal, engine
from src import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/search')
async def search(db: Session = Depends(get_db)):
    file = open('src/response_a.json')
    json_data = json.load(file)
    booking_list = list(json_data)
    segment_id = 0
    flight_id = 0
    booking_id = 0
    for booking in booking_list:
        for flight in booking['flights']:
            for segment in flight['segments']:
                dep_airport = segment['dep']['airport']
                dep_at = segment['dep']['at']
                arr_airport = segment['arr']['airport']
                arr_at = segment['arr']['at']
                segment_id += 1
                segment = {'id': segment_id,
                           'operating_airline': segment['operating_airline'],
                           'marketing_airline': segment['marketing_airline'],
                           'flight_number': segment['flight_number'],
                           'equipment': segment['equipment'],
                           'baggage': segment['baggage'],
                           'dep_airport': dep_airport,
                           'dep_at': dep_at,
                           'arr_airport': arr_airport,
                           'arr_at': arr_at}
                await create_segment(db, segment)
            flight_id += 1
            flight = {'id': flight_id,
                      'duration': flight['duration'],
                      'segment_id': segment_id}
            await create_flight(db, flight)
        booking_id += 1
        booking = {'id': booking_id,
                   'flight_id': flight_id,
                   'refundable': booking['refundable'],
                   'validating_airline': booking['validating_airline'],
                   'total_price': booking['pricing']['total'],
                   'currency': booking['pricing']['currency']}
        await create_booking(db, booking)
