from config import engine
from sqlalchemy.orm import Session, sessionmaker


def get_session():
    session: Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)()

    try:
        yield session
    finally:
        session.close()
