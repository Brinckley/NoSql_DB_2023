from typing_extensions import TypedDict
from pydantic import BaseModel, Field


class Address(TypedDict, total=False):
    country: str
    city: str
    address: str


class RoomSchema(BaseModel):
    id: int = Field(..., alias='_id')
    address: Address
    description: str = Field(...)
    attributes: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                  "_id": 1,
                  "address": [
                      {
                          "country": "Russian Federation",
                          "city": "Moscow",
                          "address": "Volokolamskoe higway, building 4"
                      }
                  ],
                  "room_id": 1,
                  "booking_date": "10.11.2023",
                  "booking_status": "paid"
            }
        }
