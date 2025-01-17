from decimal import Decimal
from uuid import UUID

from schemas import Base
from sqlmodel import UUID as SQL_UUID
from sqlmodel import Field, Relationship


class Contribution(Base, table=True):
    __tablename__ = "contributions"

    user_id: UUID = Field(sa_type=SQL_UUID(as_uuid=True), foreign_key="users.id")

    project_id: UUID = Field(sa_type=SQL_UUID(as_uuid=True), foreign_key="projects.id")

    amount: Decimal

    user: "User" = Relationship(back_populates="contributions")
    project: "Project" = Relationship(back_populates="contributions")
