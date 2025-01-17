from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from models import CreateUserOutput
from pydantic import BaseModel, Field, field_serializer, field_validator


class CreateProjectInput(BaseModel):
    title: str
    description: str
    goal_amount: Decimal = Field(..., decimal_places=2, gt=0)
    deadline: datetime

    class Config:
        from_attributes = True

    @field_validator("deadline")
    def deadline_must_be_in_future(cls, v: datetime):
        if v.tzinfo is None:
            raise ValueError("Deadline must have timezone info")
        if v <= datetime.now(timezone.utc):
            raise ValueError("Deadline must be in the future")

        return v


class CreateProjectOutput(BaseModel):
    id: UUID
    title: str
    description: str
    goal_amount: Decimal = Field(..., decimal_places=2)
    deadline: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class GetProjectOutput(BaseModel):
    id: UUID
    title: str
    description: str
    goal_amount: Decimal = Field(..., decimal_places=2)
    deadline: datetime
    created_at: datetime
    total_contributions: Decimal = Field(..., decimal_places=2)
    contributors: list[CreateUserOutput]

    @field_serializer("contributors")
    def get_contributor_usernames(self, contributors: list[CreateUserOutput]):
        return [user.username for user in contributors]

    class Config:
        from_attributes = True
