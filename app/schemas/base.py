from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlmodel import TIMESTAMP
from sqlmodel import UUID as SQL_UUID
from sqlmodel import Field, SQLModel


class Base(SQLModel):
    id: UUID = Field(
        sa_type=SQL_UUID(as_uuid=True), default_factory=uuid4, primary_key=True
    )

    created_at: datetime = Field(
        sa_type=TIMESTAMP(timezone=True), default=datetime.now(tz=timezone.utc)
    )

    updated_at: datetime = Field(
        sa_type=TIMESTAMP(timezone=True),
        default=datetime.now(tz=timezone.utc),
        sa_column_kwargs={"onupdate": datetime.now(tz=timezone.utc)},
    )

    deleted_at: datetime = Field(sa_type=TIMESTAMP(timezone=True), nullable=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def delete(self):
        self.deleted_at = datetime.now(tz=timezone.utc)
