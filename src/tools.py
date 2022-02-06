import asyncio
import uuid

from sqlalchemy.orm import Session

from src.actions import create_flight, create_booking, create_segment


async def insert_data(db: Session, booking, search_id: uuid.uuid4):
    booking_dict = {'refundable': booking['refundable'],
                    'validating_airline': booking['validating_airline'],
                    'total_price': booking['pricing']['total'],
                    'currency': booking['pricing']['currency']}
    booking_future = asyncio.Future()
    await create_booking(booking_future, db, booking_dict, search_id)
    booking_id = await booking_future
    for flight in booking['flights']:
        flight_dict = {'duration': flight['duration']}
        flight_future = asyncio.Future()
        await create_flight(flight_future, db, flight_dict, booking_id)
        flight_id = await flight_future
        for segment in flight['segments']:
            segment_dict = {'operating_airline': segment['operating_airline'],
                            'marketing_airline': segment['marketing_airline'],
                            'flight_number': int(segment['flight_number']),
                            'equipment': segment['equipment'],
                            'baggage': segment['baggage'],
                            'dep_airport': segment['dep']['airport'],
                            'dep_at': segment['dep']['at'],
                            'arr_airport': segment['arr']['airport'],
                            'arr_at': segment['arr']['at']}
            segment_future = asyncio.Future()
            await create_segment(segment_future, db, segment_dict, flight_id)


async def get_data(db: Session, booking_id):
    future = asyncio.Future()
    await get_booking(future, db, booking_id)
    col = await future
    return col
