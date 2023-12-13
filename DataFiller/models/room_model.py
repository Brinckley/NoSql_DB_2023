from typing_extensions import TypedDict
from pydantic import BaseModel


class Address(TypedDict, total=False):
    country: str
    city: str
    address: str


class RoomSchema(BaseModel):
    id: str
    full_address: Address
    description: str
    attributes: str
    booking_status: bool


class UpdateRoomSchema(BaseModel):  # class contains changeable fields for RoomSchema
    full_address: Address
    description: str
    attributes: str
    booking_status: bool
