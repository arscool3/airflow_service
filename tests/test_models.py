import uuid
from datetime import datetime
from decimal import Decimal
from pytz import timezone

from src.models import Booking, Flight, Segment, FlightSegment, BookingFlight, SearchBooking, Search, Currency


def test_init_flight_segment():
    flight_segment = FlightSegment(flight_id=1, segment_id=1)
    assert flight_segment.flight_id == 1
    assert flight_segment.segment_id == 1


def test_init_booking_flight():
    booking_flight = BookingFlight(booking_id=1, flight_id=1)
    assert booking_flight.booking_id == 1
    assert booking_flight.flight_id == 1


def test_init_search_booking():
    search_booking = SearchBooking(search_id=1, booking_id=1)
    assert search_booking.search_id == 1
    assert search_booking.booking_id == 1


def test_init_search():
    _id = uuid.uuid4()
    search = Search(id=_id, status='PENDING')
    assert search.id == _id
    assert search.status == 'PENDING'


def test_init_booking():
    booking = Booking(refundable=True,
                      validating_airline="TEST",
                      total_price=Decimal(55),
                      currency="KZT")
    assert booking.refundable == True
    assert booking.validating_airline == "TEST"
    assert booking.total_price == Decimal(55)
    assert booking.currency == "KZT"


def test_init_flight():
    flight = Flight(duration=1000)
    assert flight.duration == 1000


def test_init_segment():
    test_datetime = datetime.now(tz=timezone('Asia/Almaty'))
    segment = Segment(operating_airline='TEST',
                      marketing_airline='TEST',
                      flight_number=1,
                      equipment="TEST",
                      dep_at=test_datetime,
                      dep_airport='TEST',
                      arr_at=test_datetime,
                      arr_airport="TEST",
                      baggage="TEST")
    assert segment.operating_airline == 'TEST'
    assert segment.marketing_airline == 'TEST'
    assert segment.flight_number == 1
    assert segment.equipment == 'TEST'
    assert segment.dep_at == test_datetime
    assert segment.dep_airport == 'TEST'
    assert segment.arr_at == test_datetime
    assert segment.arr_airport == 'TEST'
    assert segment.baggage == 'TEST'


def test_init_currency():
    currency = Currency(title='KZT', amount=Decimal(1000))
    assert currency.title == 'KZT'
    assert currency.amount == Decimal(1000)
