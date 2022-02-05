import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from src.database import Base


class Booking(Base):
    __tablename__ = "booking"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    refundable = sa.Column(sa.Boolean)
    validating_airline = sa.Column(sa.String)
    total_price = sa.Column(sa.DECIMAL)
    currency = sa.Column(sa.String)


class Flight(Base):
    __tablename__ = "flight"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    duration = sa.Column(sa.Integer)


class Segment(Base):
    __tablename__ = 'segment'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    operating_airline = sa.Column(sa.String)
    marketing_airline = sa.Column(sa.String)
    flight_number = sa.Column(sa.Integer)
    equipment = sa.Column(sa.String)
    dep_at = sa.Column(sa.DateTime(timezone=True))
    dep_airport = sa.Column(sa.String)
    arr_at = sa.Column(sa.DateTime(timezone=True))
    arr_airport = sa.Column(sa.String)
    baggage = sa.Column(sa.String)


class Search(Base):
    __tablename__ = 'search'

    id = sa.Column(UUID(as_uuid=True), primary_key=True)
    status = sa.Column(sa.String, default='PENDING')
    booking_ids = sa.Column(sa.String)


class Currency(Base):
    __tablename__ = 'currency'
    id = sa.Column(sa.Integer, primary_key=True, index=True, autoincrement=True)
    title = sa.Column(sa.String)
    amount = sa.Column(sa.DECIMAL)


class FlightSegment(Base):
    __tablename__ = 'flight_segment'
    id = sa.Column(sa.Integer, primary_key=True, index=True, autoincrement=True)
    flight_id = sa.Column(sa.Integer, sa.ForeignKey('flight.id'))
    segment_id = sa.Column(sa.Integer, sa.ForeignKey('segment.id'))


class BookingFlight(Base):
    __tablename__ = 'booking_flight'
    id = sa.Column(sa.Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = sa.Column(sa.Integer, sa.ForeignKey('booking.id'))
    flight_id = sa.Column(sa.Integer, sa.ForeignKey('flight.id'))