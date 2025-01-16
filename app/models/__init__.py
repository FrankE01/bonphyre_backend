from config.database import engine
from models.base import Base
from models.contribution import Contribution
from models.project import Project
from models.user import CreateUserInput, CreateUserOutput, LoginUserInput, User

Base.metadata.create_all(bind=engine)
