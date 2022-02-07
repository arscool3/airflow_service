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


async def create_booking(future: asyncio.Future, db: database, booking: Booking, search_id):
    booking_stmt = insert(BookingTbl).values(booking.as_dict())
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


async def get_search(future: asyncio.Future, db: database, search_id, currency):
    stmt = select(BookingTbl).where(SearchBookingTbl.c.search_id == search_id,
                                    BookingTbl.c.id == SearchBookingTbl.c.booking_id)
    bookings = await db.fetch_all(stmt)
    unique_bookings = []
    for row in bookings:
        unique_bookings.append(dict(zip(row.keys(), row.values())))
    res = []
    main_currency = await get_currency_by_title(database, currency)
    for booking in unique_bookings:
        currency = await get_currency_by_title(database, booking['currency'])

        amount = booking['total_price'] * currency.amount / main_currency.amount
        booking_dict = {'id': booking['id'],
                        'booking': Booking(booking['refundable'], booking['validating_airline'], amount, 'KZT')}
        res.append(booking_dict)
    future.set_result(res)


async def create_currency(db: database, currency: Currency):
    stmt = insert(CurrencyTbl).values(currency.as_dict())
    await db.execute(stmt)


async def get_currency_by_title(db: database, title: str) -> Currency:
    stmt = select(CurrencyTbl.c.title, CurrencyTbl.c.amount).where(CurrencyTbl.c.title == title)
    currency_data = await db.fetch_one(stmt)
    return Currency(title=currency_data['title'],
                    amount=currency_data['amount'])
