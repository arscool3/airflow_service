import asyncio
from sqlalchemy.orm import Session

from src import models


async def create_flight(future: asyncio.Future, db: Session, flight: dict):
    db_flight = models.Flight(id=flight['id'],
                              duration=flight['id'])

    db_flight_segment = models.FlightSegment(flight_id=flight['id'],
                                             segment_id=flight['segment_id'])
    db.add(db_flight)
    db.add(db_flight_segment)
    db.commit()
    db.refresh(db_flight)
    db.refresh(db_flight_segment)
    await db_flight


async def create_segment(future: asyncio.Future, db: Session, segment: dict):
    db_segment = models.Segment(id=segment['id'],
                                operating_airline=segment['operating_airline'],
                                marketing_airline=segment['marketing_airline'],
                                flight_number=segment['flight_number'],
                                equipment=segment['equipment'],
                                dep_at=segment['dep_at'],
                                dep_airport=segment['dep_airport'],
                                arr_at=segment['arr_at'],
                                arr_airport=segment['arr_airport'],
                                baggage=segment['baggage'])

    db.add(db_segment)
    db.commit()
    db.refresh(db_segment)


async def create_booking(future: asyncio.Future, db: Session, booking: dict):
    db_booking = models.Booking(id=booking['id'],
                                refundable=booking['refundable'],
                                validating_airline=booking['validating_airline'],
                                total_price=booking['total_price'],
                                currency=booking['currency'])
    db_booking_flight = models.BookingFlight(booking_id=booking['id'],
                                             flight_id=booking['flight_id'])
    db.add(db_booking)
    db.add(db_booking_flight)
    db.commit()
    db.refresh(db_booking)
    db.refresh(db_booking_flight)
