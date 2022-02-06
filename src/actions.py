import asyncio
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert

from src import models


async def create_flight(future: asyncio.Future, db: Session, flight: dict):
    db_flight = models.Flight(duration=flight['duration'])

    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    db_booking_flight = models.BookingFlight(booking_id=flight['booking_id'],
                                             flight_id=db_flight.id)

    db.add(db_booking_flight)
    db.commit()
    db.refresh(db_booking_flight)
    future.set_result(db_flight.id)


async def create_segment(future: asyncio.Future, db: Session, segment: dict):
    db_segment = models.Segment(operating_airline=segment['operating_airline'],
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

    db_flight_segment = models.FlightSegment(flight_id=segment['flight_id'],
                                             segment_id=db_segment.id)
    db.add(db_flight_segment)
    db.commit()
    db.refresh(db_flight_segment)

    future.set_result(db_segment)


async def create_booking(future: asyncio.Future, db: Session, booking: dict):
    db_booking = models.Booking(refundable=booking['refundable'],
                                validating_airline=booking['validating_airline'],
                                total_price=booking['total_price'],
                                currency=booking['currency'])

    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    db_search_booking = models.SearchBooking(search_id=booking['search_id'],
                                             booking_id=db_booking.id)
    db.add(db_search_booking)
    db.commit()
    db.refresh(db_search_booking)

    future.set_result(db_booking.id)


async def get_booking(future: asyncio.Future, db: Session, booking_id: int):
    query = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    future.set_result(query)


async def create_search(db: Session, search: dict):
    db_search = models.Search(id=search['id'],
                              status=search['status'])

    db.add(db_search)
    db.commit()
    db.refresh(db_search)


async def update_search(db: Session, search_id: uuid.uuid4):
    stmt = update(models.Search).where(models.Search.id == search_id).values(status='COMPLETED')
    db.execute(stmt)
    db.commit()


async def get_search(future: asyncio.Future, db: Session, search_id):
    stmt = select(models.Booking.id,
                  models.Booking.refundable,
                  models.Booking.validating_airline,
                  models.Booking.currency,
                  models.Booking.total_price).where(models.SearchBooking.search_id == search_id,
                                                    models.Booking.id == models.SearchBooking.booking_id)
    bookings = set(db.execute(stmt).fetchall())
    res = []
    for booking in bookings:
        course_stmt = select(models.Currency.amount).where(models.Currency.title == booking['currency'])
        course = db.execute(course_stmt).first()
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


async def create_currency(db: Session, currency: dict):
    db_currency = models.Currency(title=currency['title'],
                                  amount=currency['amount'])
    db.add(db_currency)
    db.commit()
    db.refresh(db_currency)


async def get_currency_by_title(db: Session, title: str):
    query = db.query(models.Currency.amount).filter(models.Currency.title == title).first()
    return query
