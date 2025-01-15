import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("bonphyre")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(
            "../logs/bonfire_backend.log",
            maxBytes=10000000,
            backupCount=3
        )
    ]
)