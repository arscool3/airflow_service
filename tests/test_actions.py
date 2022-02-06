import datetime
import uuid

import databases
import pytest
import sqlalchemy as sa
import asyncio

from src.models import Search, Segment
from src.database import SearchTbl, SegmentTbl
from src.actions import create_flight, create_search, create_segment

SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin@localhost:5438/airflow_service"

database = databases.Database(SQLALCHEMY_DATABASE_URL)

metadata = sa.MetaData()


@pytest.mark.asyncio
async def test_create_flight():
    await database.connect()
    future = asyncio.Future()
    await create_flight(future, database, {'duration': 1500})


@pytest.mark.asyncio
async def test_create_search():
    await database.connect()
    _id = uuid.uuid4()
    search = Search(_id, 'TEST')
    await create_search(database, search)
    stmt = sa.select(SearchTbl.c.status,
                     SearchTbl.c.id).where(SearchTbl.c.id == _id)
    res = await database.fetch_one(stmt)
    assert res['status'] == 'TEST'


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
    future = asyncio.Future()
    await create_segment(future, database, segment, 1)
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


