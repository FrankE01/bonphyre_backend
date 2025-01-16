from uuid import UUID, uuid4

from sqlmodel import UUID as SQL_UUID
from sqlmodel import Field, SQLModel


class Contribution(SQLModel, table=True):
    __tablename__ = "contributions"

    user_id: UUID = Field(
        sa_type=SQL_UUID(as_uuid=True), primary_key=True, foreign_key="users.id"
    )

    project_id: UUID = Field(
        sa_type=SQL_UUID(as_uuid=True), primary_key=True, foreign_key="projects.id"
    )

    amount: float = Field(decimal_places=2)
