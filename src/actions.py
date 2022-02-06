import asyncio
import uuid

from src.database import database
from sqlalchemy import select, update, insert

from src.database import (FlightTbl, BookingFlightTbl, SegmentTbl, FlightSegmentTbl,
                          SearchBookingTbl, SearchTbl, CurrencyTbl, BookingTbl)

from src.models import (Flight, BookingFlight, Search, FlightSegment,
                        SearchBooking, Segment, Currency, Booking)


async def create_flight(future: asyncio.Future, db: database, flight: Flight, booking_id: int):
    flight_stmt = insert(FlightTbl).values(flight.as_dict())
    flight_id = await db.execute(flight_stmt)
    booking_flight_stmt = insert(BookingFlightTbl).values(booking_id=booking_id,
                                                          flight_id=flight_id)
    await db.execute(booking_flight_stmt)
    future.set_result(flight_id)


async def create_segment(future: asyncio.Future, db: database, segment: Segment, flight_id):
    segment_stmt = insert(SegmentTbl).values(segment.as_dict())
    segment_id = await db.execute(segment_stmt)

    db_flight_segment = insert(FlightSegmentTbl).values(flight_id=flight_id,
                                                        segment_id=segment_id)
    await db.execute(db_flight_segment)
    future.set_result(segment_id)


async def create_booking(future: asyncio.Future, db: database, booking: dict, search_id):
    booking_stmt = insert(BookingTbl).values(**booking)
    booking_id = await db.execute(booking_stmt)

    db_search_booking = insert(SearchBookingTbl).values(search_id=search_id,
                                                        booking_id=booking_id)
    await db.execute(db_search_booking)
    future.set_result(booking_id)


async def create_search(db: database, search: Search):
    db_search = insert(SearchTbl).values(search.as_dict())
    await db.execute(db_search)



async def update_search(db: database, search_id: uuid.uuid4):
    stmt = update(SearchTbl).where(SearchTbl.c.id == search_id).values(status='COMPLETED')
    await db.execute(stmt)


async def get_search(future: asyncio.Future, db: database, search_id):
    stmt = select(BookingTbl.c.id,
                  BookingTbl.c.refundable,
                  BookingTbl.c.validating_airline,
                  BookingTbl.c.currency,
                  BookingTbl.c.total_price).where(SearchBookingTbl.c.search_id == search_id,
                                                  BookingTbl.c.id == SearchBookingTbl.c.booking_id)
    bookings = await db.execute(stmt).fetchall()
    unique_bookings = set(bookings)
    res = []
    for booking in unique_bookings:
        course_stmt = select(CurrencyTbl.c.amount).where(CurrencyTbl.c.title == booking['currency'])
        course = await db.execute(course_stmt).first()
        if course is None:
            amount = booking['total_price']
        else:
            amount = booking['total_price'] * course['amount']
        booking_dict = {'id': booking['id'],
                        'refundable': booking['refundable'],
                        'validating_airline': booking['validating_airline'],
                        'total_price': amount,
                        'currency': 'KZT'}
        res.append(booking_dict)
    future.set_result(res)


async def create_currency(db: database, currency: dict):
    stmt = insert(CurrencyTbl).values(**currency)
    await db.execute(stmt)


async def get_currency_by_title(db: database, title: str):
    query = db.query(CurrencyTbl.c.amount).filter(CurrencyTbl.c.title == title).first()
    return query
