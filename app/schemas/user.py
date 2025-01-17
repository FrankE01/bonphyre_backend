from schemas import Base, Contribution
from sqlmodel import Field, Relationship


class User(Base, table=True):
    __tablename__ = "users"

    username: str = Field(unique=True, max_length=50)
    email: str = Field(unique=True)
    password: str

    contributions: list[Contribution] = Relationship(back_populates="user")
    projects: list["Project"] = Relationship(
        link_model=Contribution, sa_relationship_kwargs={"viewonly": True}
    )

    def __repr__(self):
        return f"<User(username={self.username!r}, email={self.email!r})>"
