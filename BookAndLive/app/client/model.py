from pydantic import BaseModel, EmailStr, Field


class ClientSchema(BaseModel):
    id: int = Field(..., alias='_id')
    name: str
    email: EmailStr


class UpdateClientSchema(BaseModel):  # class contains changeable fields for ClientSchema
    name: str
    email: EmailStr
