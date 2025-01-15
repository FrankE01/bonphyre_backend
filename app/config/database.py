import os

from config import logger
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not database_exists(DATABASE_URL):
    create_database(DATABASE_URL)

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        logger.info("Database Connection Successful.")
except Exception as e:
    logger.error(f"Database Connection Failed: {str(e)}")