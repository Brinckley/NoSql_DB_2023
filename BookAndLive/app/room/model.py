from typing_extensions import TypedDict
from pydantic import BaseModel, Field


class Address(TypedDict, total=False):
    country: str
    city: str
    address: str


class RoomSchema(BaseModel):
    id: int = Field(..., alias='_id')
    address: Address
    description: str
    attributes: str
    booking_status: bool


class UpdateRoomSchema(BaseModel):  # class contains changeable fields for RoomSchema
    description: str
    attributes: str
    booking_status: bool
