from datetime import datetime, timezone
from decimal import Decimal

from schemas import Base, Contribution
from sqlmodel import TIMESTAMP, Field, Relationship


class Project(Base, table=True):
    __tablename__ = "projects"

    title: str = Field(unique=True, max_length=100)
    description: str = Field(unique=True, max_length=1000)
    goal_amount: Decimal
    deadline: datetime = Field(sa_type=TIMESTAMP(timezone=True))

    contributions: list[Contribution] = Relationship(back_populates="project")
    contributors: list["User"] = Relationship(
        link_model=Contribution, sa_relationship_kwargs={"viewonly": True}
    )

    @property
    def total_contributions(self) -> Decimal:
        return sum([contribution.amount for contribution in self.contributions])

    def __repr__(self):
        return f"<Project(title={self.title!r}, goal_amount={self.goal_amount!r})>"
