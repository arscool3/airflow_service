import asyncio
import uuid

from sqlalchemy.orm import Session

from src.models import Booking, Segment, Flight
from src.actions import create_flight, create_booking, create_segment
from src.database import database


async def insert_data(db: database, booking, search_id: uuid.uuid4):
    booking_ins = Booking(booking['refundable'],
                          booking['validating_airline'],
                          booking['pricing']['total'],
                          booking['pricing']['currency'])
    booking_future = asyncio.Future()
    await create_booking(booking_future, db, booking_ins, search_id)
    booking_id = await booking_future
    for flight in booking['flights']:
        flight_ins = Flight(flight['duration'])
        flight_future = asyncio.Future()
        await create_flight(flight_future, db, flight_ins, booking_id)
        flight_id = await flight_future
        for segment in flight['segments']:
            segment_ins = Segment(segment['operating_airline'],
                                  segment['marketing_airline'],
                                  int(segment['flight_number']),
                                  segment['equipment'],
                                  segment['baggage'],
                                  segment['dep']['airport'],
                                  segment['dep']['at'],
                                  segment['arr']['airport'],
                                  segment['arr']['at'])
            segment_future = asyncio.Future()
            await create_segment(segment_future, db, segment_ins, flight_id)
