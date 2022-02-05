from datetime import datetime
from decimal import Decimal
from pytz import timezone

from src.models import Booking, Flight, Segment


def test_init_booking():
    booking = Booking(id=1,
                      refundable=True,
                      validating_airline="TEST",
                      total_price=Decimal(50),
                      currency="KZT")
    assert booking.id == 1
    assert booking.refundable == True
    assert booking.validating_airline == "TEST"
    assert booking.total_price == Decimal(50)
    assert booking.currency == "KZT"


def test_init_flight():
    flight = Flight(id=1,
                    duration=1500)
    assert flight.id == 1
    assert flight.duration == 1500


def test_init_segment():
    test_datetime = datetime.now(tz=timezone('Asia/Almaty'))
    segment = Segment(id=1,
                      operating_airline='TEST',
                      marketing_airline='TEST',
                      flight_number=1,
                      equipment="TEST",
                      dep_at=test_datetime,
                      dep_airport='TEST',
                      arr_at=test_datetime,
                      arr_airport="TEST",
                      baggage="TEST")
    assert segment.id == 1
    assert segment.operating_airline == 'TEST'
    assert segment.marketing_airline == 'TEST'
    assert segment.flight_number == 1
    assert segment.equipment == 'TEST'
    assert segment.dep_at == test_datetime
    assert segment.dep_airport == 'TEST'
    assert segment.arr_at == test_datetime
    assert segment.arr_airport == 'TEST'
    assert segment.baggage == 'TEST'
