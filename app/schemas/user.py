from schemas import Base, Contribution
from sqlmodel import Field, Relationship

class User(Base, table=True):
    __tablename__ = "users"

    username: str = Field(unique=True,max_length=50)
    email: str = Field(unique=True, regex=r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$")
    password: str

    projects: list["Project"] = Relationship(link_model=Contribution, back_populates="users")

    def __repr__(self):
        return f"<User(username={self.username!r}, email={self.email!r})>"
