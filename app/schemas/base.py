
from sqlmodel import SQLModel, Field, DateTime, UUID as SQL_UUID
from uuid import UUID, uuid4
from datetime import datetime, timezone

class Base(SQLModel):
    id: UUID = Field(sa_type=SQL_UUID(as_uuid=True), default_factory=uuid4, primary_key=True)

    created_at: datetime = Field(sa_type=DateTime, default=datetime.now(tz=timezone.utc))

    updated_at: datetime = Field(sa_type=DateTime, default=datetime.now(tz=timezone.utc), onupdate=datetime.now(tz=timezone.utc))

    deleted_at: datetime = Field(sa_type=DateTime, nullable=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def delete(self):
        self.deleted_at = datetime.now(tz=timezone.utc)