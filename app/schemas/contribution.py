from sqlmodel import SQLModel, Field, UUID as SQL_UUID
from uuid import uuid4

class Contribution(SQLModel, table=True):
    __tablename__ = "contributions"

    user_id = Field(sa_type=SQL_UUID(as_uuid=True), primary_key=True, foreign_key="users.id")

    project_id = Field(sa_type=SQL_UUID(as_uuid=True), primary_key=True, foreign_key="projects.id")

    amount: float = Field(decimal_places=2)