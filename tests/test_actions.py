import databases
import pytest
import sqlalchemy as sa
import asyncio

from src.actions import create_flight

SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin@localhost:5438/airflow_service"

database = databases.Database(SQLALCHEMY_DATABASE_URL)

metadata = sa.MetaData()


@pytest.mark.asyncio
async def test_create_flight():
    await database.connect()
    future = asyncio.Future()
    await create_flight(future, database, {'duration': 1500})

