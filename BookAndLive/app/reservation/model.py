from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class BookStatusEnum(str, Enum):
    default = "default"  # default status
    unpaid = "unpaid"  # client booked the room, but hasn't paid for it yet
    paid = "paid"  # room is booked and paid


class ReservationSchema(BaseModel):
    id: str
    client_id: str
    room_id: str
    booking_date: datetime = None
    booking_status: BookStatusEnum = BookStatusEnum.default


class UpdateReservationSchema(BaseModel):  # class contains changeable fields for ReservationSchema
    client_id: str
    room_id: str
    booking_date: datetime = None
    booking_status: BookStatusEnum = BookStatusEnum.default
