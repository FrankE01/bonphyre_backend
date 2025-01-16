from datetime import datetime

from models import Base, Contribution
from sqlmodel import Field, Relationship


class Project(Base, table=True):
    __tablename__ = "projects"

    title: str = Field(unique=True, max_length=100)
    description: str = Field(unique=True, max_length=1000)
    goal_amount: float = Field(decimal_places=2)
    deadline: datetime

    users: list["User"] = Relationship(
        link_model=Contribution, back_populates="projects"
    )

    def __repr__(self):
        return f"<Project(title={self.title!r})>"
