from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class BookStatusEnum(str, Enum):
    default = "default"  # default status
    unpaid = "unpaid"  # client booked the room, but hasn't paid for it yet
    paid = "paid"  # room is booked and paid


class ReservationSchema(BaseModel):
    id: int = Field(..., alias='_id')
    client_id: int = Field(...)
    room_id: int = Field(...)
    booking_date: datetime = None
    booking_status: BookStatusEnum = BookStatusEnum.default


class UpdateReservationSchema(BaseModel):  # class contains changeable fields for ReservationSchema
    booking_date: datetime = None
    booking_status: BookStatusEnum = BookStatusEnum.default

    class Config:
        schema_extra = {
            "example": {
                  "_id": 1,
                  "client_id": 1,
                  "room_id": 1,
                  "booking_date": "10.11.2023",
                  "booking_status": "paid"
            }
        }
