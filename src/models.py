import uuid
from decimal import Decimal
from datetimei import datetime


class FlightSegment:
    def __init__(self, _id: int, flight_id: int, segment_id: int):
        self.id = _id
        self.flight_id = flight_id
        self.segment_id = segment_id


class BookingFlight:
    def __init__(self, _id: int, booking_id: int, flight_id: int):
        self.id = _id
        self.booking_id = booking_id
        self.flight_id = flight_id


class SearchBooking:
    def __init__(self, _id: int, search_id: uuid.uuid4, booking_id: int):
        self.id = _id
        self.search_id = search_id
        self.booking_id = booking_id


class Search:
    def __init__(self, _id: uuid.uuid4, status: str):
        self.id = _id  # TODO переделать на Enum
        self.status = status


class Booking:
    def __init__(self, _id: int, refundable: bool, validating_airline: str, total_price: Decimal, currency: str):
        self.id = _id
        self.refundable = refundable
        self.validating_airline = validating_airline
        self.total_price = total_price
        self.currency = currency


class Flight:
    def __init__(self, _id: int, duration: int):
        self.id = _id
        self.duration = duration


class Segment:
    def __init__(self, _id: int, operating_airline: str, marketing_airline: str,
                 flight_number: int, equipment: str, dep_at: datetime,
                 dep_airport: str, arr_at: datetime, arr_airport: str, baggage: str):
        self.id = _id
        self.operating_airline = operating_airline
        self.marketing_airline = marketing_airline
        self.flight_number = flight_number
        self.equipment = equipment
        self.dep_at = dep_at
        self.dep_airport = dep_airport
        self.arr_at = arr_at
        self.arr_airport = arr_airport
        self.baggage = baggage


class Currency:
    def __init__(self, _id: int, title: str, amount: Decimal):
        self.id = _id
        self.title = title
        self.amount = amount
