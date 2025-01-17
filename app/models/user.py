import re
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CreateUserInput(BaseModel):
    username: str
    email: str = Field(
        pattern=r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", examples=["string"]
    )
    password: str

    class Config:
        from_attributes = True


class CreateUserOutput(BaseModel):
    id: UUID
    email: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class LoginUserInput(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True
