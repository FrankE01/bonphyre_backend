from datetime import datetime
from decimal import Decimal

from models import CreateProjectOutput, CreateUserOutput
from pydantic import BaseModel, Field


class CreateContributionOUtput(BaseModel):
    user: CreateUserOutput
    project: CreateProjectOutput
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    created_at: datetime
