from config import engine
from sqlalchemy.orm import sessionmaker


def get_session():
    session = sessionmaker(autoflush=False, autocommit=False, bind=engine)()

    try:
        yield session
    finally:
        session.close()
