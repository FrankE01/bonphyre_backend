import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from main import app
from schemas import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists
from utils import get_session


@pytest.fixture(scope="function")
def test_client():
    """
    Fixture to provide a test client for FastAPI.
    """
    client = TestClient(app)
    yield client


@pytest.fixture(scope="function")
def setup_db():
    """
    Fixture to set up the test database before each test and clean it up after.
    """

    load_dotenv()

    DATABASE_URL = os.getenv("TEST_DATABASE_URL")

    if not database_exists(DATABASE_URL):
        create_database(DATABASE_URL)

    engine = create_engine(DATABASE_URL)

    Base.metadata.create_all(bind=engine)

    session = Session(bind=engine)

    app.dependency_overrides[get_session] = lambda: session

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)
