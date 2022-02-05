import asyncio
from sqlalchemy.orm import Session

from src.actions import create_flight, create_booking, create_segment, get_booking


async def insert_data(db: Session, booking, booking_id: int):

    segment_id = booking_id * 2
    flight_id = booking_id * 2

    for flight in booking['flights']:
        for segment in flight['segments']:
            segment = {'id': segment_id,
                       'operating_airline': segment['operating_airline'],
                       'marketing_airline': segment['marketing_airline'],
                       'flight_number': segment['flight_number'],
                       'equipment': segment['equipment'],
                       'baggage': segment['baggage'],
                       'dep_airport': segment['dep']['airport'],
                       'dep_at': segment['dep']['at'],
                       'arr_airport': segment['arr']['airport'],
                       'arr_at': segment['arr']['at']}
            segment_future = asyncio.Future()
            await create_segment(segment_future, db, segment)
        flight = {'id': flight_id,
                  'duration': flight['duration'],
                  'segment_id': segment_id}
        flight_future = asyncio.Future()
        await create_flight(flight_future, db, flight)
    booking = {'id': booking_id,
               'flight_id': flight_id,
               'refundable': booking['refundable'],
               'validating_airline': booking['validating_airline'],
               'total_price': booking['pricing']['total'],
               'currency': booking['pricing']['currency']}
    booking_future = asyncio.Future()
    await create_booking(booking_future, db, booking)


async def get_data(db: Session, booking_id):
    future = asyncio.Future()
    await get_booking(future, db, booking_id)
    col = await future
    return col

