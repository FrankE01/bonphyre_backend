import re
from datetime import datetime
from uuid import UUID

from models import Base, Contribution
from pydantic import BaseModel
from pydantic import Field as PyField
from sqlmodel import Field, Relationship


class User(Base, table=True):
    __tablename__ = "users"

    username: str = Field(unique=True, max_length=50)
    email: str = Field(unique=True)
    password: str

    projects: list["Project"] = Relationship(
        link_model=Contribution, back_populates="users"
    )

    def __repr__(self):
        return f"<User(username={self.username!r}, email={self.email!r})>"


class CreateUserInput(BaseModel):
    username: str
    email: str = PyField(pattern=r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", examples=["string"])
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
