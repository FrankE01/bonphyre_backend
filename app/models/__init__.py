from config.database import engine
from models.base import Base
from models.contribution import Contribution
from models.project import Project
from models.user import CreateUserInput, CreateUserOutput, User, LoginUserInput

Base.metadata.create_all(bind=engine)
