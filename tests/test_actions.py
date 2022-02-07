import datetime
import uuid

import databases
import pytest
import json
import sqlalchemy as sa
import asyncio

from decimal import Decimal

from src.tools import insert_data
from src.models import Search, Segment, Flight, Currency, Booking
from src.database import SearchTbl, SegmentTbl, CurrencyTbl, FlightTbl, BookingTbl
from src.actions import (create_flight, create_search, create_segment, create_booking, update_search,
                         create_currency, get_currency_by_title, get_search)

SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin@localhost:5438/airflow_service"

database = databases.Database(SQLALCHEMY_DATABASE_URL)

metadata = sa.MetaData()

file = open('test_data.json')
json_data = json.load(file)


@pytest.mark.asyncio
async def test_create_flight():
    await database.connect()
    booking = Booking(refundable=True,
                      validating_airline='TEST',
                      total_price=Decimal(500),
                      currency="KZT")
    insert_stmt = sa.insert(BookingTbl).values(booking.as_dict())
    booking_id = await database.execute(insert_stmt)
    future = asyncio.Future()
    flight = Flight(1500)
    await create_flight(future, database, flight, booking_id)
    flight_id = await future
    stmt = sa.select(FlightTbl.c.duration).where(FlightTbl.c.id == flight_id)
    res = await database.fetch_one(stmt)
    res_flight = Flight(**res)
    assert res_flight.duration == 1500


@pytest.mark.asyncio
async def test_create_segment():
    await database.connect()
    cur_date = datetime.datetime.now()
    segment = Segment(operating_airline='TEST',
                      marketing_airline='TEST',
                      flight_number=123,
                      equipment='TEST',
                      dep_at=str(cur_date),
                      dep_airport='TEST',
                      arr_at=str(cur_date),
                      arr_airport='TEST',
                      baggage='TEST')

    flight = Flight(duration=1500)
    insert_stmt = sa.insert(FlightTbl).values(flight.as_dict())
    flight_id = await database.execute(insert_stmt)

    future = asyncio.Future()
    await create_segment(future, database, segment, flight_id)
    segment_id = await future
    stmt = sa.select(SegmentTbl.c.operating_airline,
                     SegmentTbl.c.marketing_airline,
                     SegmentTbl.c.flight_number,
                     SegmentTbl.c.equipment,
                     SegmentTbl.c.dep_at,
                     SegmentTbl.c.dep_airport,
                     SegmentTbl.c.arr_at,
                     SegmentTbl.c.arr_airport,
                     SegmentTbl.c.baggage).where(SegmentTbl.c.id == segment_id)
    res = await database.fetch_one(stmt)
    res_segment = Segment(**res)
    assert isinstance(res_segment, Segment)
    assert res_segment.operating_airline == segment.operating_airline
    assert res_segment.marketing_airline == segment.marketing_airline
    assert res_segment.flight_number == segment.flight_number
    assert res_segment.equipment == segment.equipment
    assert res_segment.dep_at == segment.dep_at
    assert res_segment.dep_airport == segment.dep_airport
    assert res_segment.arr_airport == segment.arr_airport
    assert res_segment.arr_at == segment.arr_at
    assert res_segment.baggage == segment.baggage


@pytest.mark.asyncio
async def test_create_booking():
    await database.connect()
    booking = Booking(refundable=True,
                      validating_airline='TEST',
                      total_price=Decimal(500),
                      currency='KZT')

    search = Search(id=uuid.uuid4(), status='TEST')
    insert_stmt = sa.insert(SearchTbl).values(search.as_dict())
    await database.execute(insert_stmt)

    future = asyncio.Future()
    await create_booking(future, database, booking, search.id)
    booking_id = await future
    stmt = sa.select(BookingTbl.c.refundable,
                     BookingTbl.c.validating_airline,
                     BookingTbl.c.total_price,
                     BookingTbl.c.currency).where(BookingTbl.c.id == booking_id)
    res = await database.fetch_one(stmt)
    res_booking = Booking(**res)
    assert res_booking.refundable == booking.refundable
    assert res_booking.validating_airline == booking.validating_airline
    assert res_booking.total_price == booking.total_price
    assert res_booking.currency == booking.currency


@pytest.mark.asyncio
async def test_create_search():
    await database.connect()
    _id = uuid.uuid4()
    search = Search(_id, 'PENDING')
    await create_search(database, search)
    stmt = sa.select(SearchTbl.c.status).where(SearchTbl.c.id == _id)
    res = await database.fetch_one(stmt)
    assert res['status'] == 'PENDING'


@pytest.mark.asyncio
async def test_update_search():
    await database.connect()
    search = Search(uuid.uuid4(), 'PENDING')
    insert_stmt = sa.insert(SearchTbl).values(search.as_dict())
    await database.execute(insert_stmt)
    await update_search(database, search.id)
    stmt = sa.select(SearchTbl.c.status).where(SearchTbl.c.id == search.id)
    res = await database.fetch_one(stmt)
    assert res['status'] == 'COMPLETED'


@pytest.mark.asyncio
async def test_create_currency():
    await database.connect()
    currency = Currency('KZT', 1)
    await create_currency(database, currency)
    stmt = sa.select(CurrencyTbl.c.title,
                     CurrencyTbl.c.amount).where(CurrencyTbl.c.title == currency.title)
    currency_data = await database.fetch_one(stmt)
    res_currency = Currency(**currency_data)
    assert res_currency.title == 'KZT'
    assert res_currency.amount == 1


@pytest.mark.asyncio
async def test_get_currency_by_title():
    await database.connect()
    currency = Currency('KZT', 1)
    stmt = sa.insert(CurrencyTbl).values(currency.as_dict())
    await database.execute(stmt)
    res_currency: Currency = await get_currency_by_title(database, currency.title)

    assert res_currency.amount == currency.amount
    assert res_currency.title == currency.title


@pytest.mark.asyncio
async def test_insert_data():
    await database.connect()

    search = Search(id=uuid.uuid4(), status='PENDING')
    stmt = sa.insert(SearchTbl).values(search.as_dict())
    await database.execute(stmt)

    await insert_data(database, json_data, search.id)
    booking_stmt = sa.select(BookingTbl)
    res = await database.fetch_one(booking_stmt)
    assert res['validating_airline'] == 'KC'
    assert res['total_price'] == Decimal('291.84')
    assert res['currency'] == 'EUR'
