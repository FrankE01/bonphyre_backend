# isort:skip_file

from config.database import engine
from schemas.base import Base
from schemas.contribution import Contribution
from schemas.user import User
from schemas.project import Project

Base.metadata.create_all(bind=engine)
