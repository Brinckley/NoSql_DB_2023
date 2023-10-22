from pydantic import BaseModel, EmailStr, Field


class ClientSchema(BaseModel):
    id: int = Field(..., alias='_id')
    name: str = Field(...)
    email: EmailStr = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "_id": "1",
                "name": "Jhon Smith",
                "email": "jdoe@x.edu.ng",
            }
        }
