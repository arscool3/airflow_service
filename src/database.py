from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import databases
import sqlalchemy as sa

SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin@localhost:5438/airflow_service"

database = databases.Database(SQLALCHEMY_DATABASE_URL)

metadata = sa.MetaData()

FlightSegmentTbl = sa.Table(
    "flight_segment",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("flight_id", sa.Integer, sa.ForeignKey("flight.id")),
    sa.Column("segment_id", sa.Integer, sa.ForeignKey("segment.id"))
)

BookingFlightTbl = sa.Table(
    "booking_flight",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("booking_id", sa.Integer, sa.ForeignKey("booking.id")),
    sa.Column("flight_id", sa.Integer, sa.ForeignKey("flight.id"))
)

SearchBookingTbl = sa.Table(
    "search_booking",
    metadata,
    sa.Column("search_booking", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("search_id", UUID(as_uuid=True), sa.ForeignKey("search.id")),
    sa.Column("booking_id", sa.Integer, sa.ForeignKey("booking.id"))
)
SearchTbl = sa.Table(
    "search",
    metadata,
    sa.Column("id", UUID(as_uuid=True), primary_key=True),
    sa.Column("status", sa.String, default="PENDING")
)

BookingTbl = sa.Table(
    "booking",
    metadata,
    sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
    sa.Column("refundable", sa.Boolean),
    sa.Column("validating_airline", sa.String),
    sa.Column("total_price", sa.DECIMAL),
    sa.Column("currency", sa.String),

)

FlightTbl = sa.Table(
    "flight",
    metadata,
    sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
    sa.Column("duration", sa.Integer)
)

SegmentTbl = sa.Table(
    "segment",
    metadata,
    sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
    sa.Column("operating_airline", sa.String),
    sa.Column("marketing_airline", sa.String),
    sa.Column("flight_number", sa.Integer),
    sa.Column("equipment", sa.String),
    sa.Column("dep_at", sa.String),
    sa.Column("dep_airport", sa.String),
    sa.Column("arr_at", sa.String),
    sa.Column("arr_airport", sa.String),
    sa.Column("baggage", sa.String)
)

CurrencyTbl = sa.Table(
    "currency",
    metadata,
    sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
    sa.Column("title", sa.String),
    sa.Column("amount", sa.DECIMAL)
)

engine = sa.create_engine(
    SQLALCHEMY_DATABASE_URL
)
metadata.create_all(engine)
