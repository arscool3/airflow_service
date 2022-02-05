from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Booking(BaseModel):
    class Config:
        orm_mode = True

    id: int
    flight_id: int
    refundable: bool
    validating_airline: str
    total_price: Decimal
    currency: str


class Flight(BaseModel):
    id: int
    duration: int
    segment_id: int

    class Config:
        orm_mode = True


class Segment(BaseModel):
    class Config:
        orm_mode = True

    id: int
    operating_airline: str
    marketing_airline: str
    flight_number: int
    equipment: str
    dep_airport: str
    arr_airport: str
    baggage: str = ''
    dep_at: datetime
    arr_at: datetime
