import uuid
from decimal import Decimal
from datetime import datetime


class FlightSegment:
    def __init__(self, flight_id: int, segment_id: int):
        self.flight_id = flight_id
        self.segment_id = segment_id


class BookingFlight:
    def __init__(self, booking_id: int, flight_id: int):
        self.booking_id = booking_id
        self.flight_id = flight_id


class SearchBooking:
    def __init__(self, search_id: uuid.uuid4, booking_id: int):
        self.search_id = search_id
        self.booking_id = booking_id


class Search:
    def __init__(self, id: uuid.uuid4, status: str):
        # TODO переделать на Enum
        self.id = id
        self.status = status

    def as_dict(self):
        return dict(id=self.id,
                    status=self.status)


class Booking:
    def __init__(self, refundable: bool, validating_airline: str, total_price: Decimal, currency: str):
        self.refundable = refundable
        self.validating_airline = validating_airline
        self.total_price = total_price
        self.currency = currency


class Flight:
    def __init__(self, duration: int):
        self.duration = duration


class Segment:
    def __init__(self, operating_airline: str, marketing_airline: str,
                 flight_number: int, equipment: str, dep_at: datetime,
                 dep_airport: str, arr_at: datetime, arr_airport: str, baggage: str):
        self.operating_airline = operating_airline
        self.marketing_airline = marketing_airline
        self.flight_number = flight_number
        self.equipment = equipment
        self.dep_at = dep_at
        self.dep_airport = dep_airport
        self.arr_at = arr_at
        self.arr_airport = arr_airport
        self.baggage = baggage

    def as_dict(self):
        return dict(operating_airline=self.operating_airline,
                    marketing_airline=self.marketing_airline,
                    flight_number=self.flight_number,
                    equipment=self.equipment,
                    dep_at=self.dep_at,
                    dep_airport=self.dep_airport,
                    arr_at=self.arr_at,
                    arr_airport=self.arr_airport,
                    baggage=self.baggage)


class Currency:
    def __init__(self, title: str, amount: Decimal):
        self.title = title
        self.amount = amount
