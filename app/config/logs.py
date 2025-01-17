import logging
import os
import time
from logging.handlers import RotatingFileHandler

from fastapi import Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("bonphyre")

logging.getLogger("passlib").setLevel(logging.ERROR)
logging.getLogger("watchfiles.main").setLevel(logging.ERROR)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(
            os.path.join(BASE_DIR, "logs", "bonphyre_backend.log"),
            maxBytes=10000000,
            backupCount=3,
        ),
    ],
)


class Log_Requests(BaseHTTPMiddleware):
    def __init__(self, app, dispatch=None):
        super().__init__(app, dispatch)

    async def dispatch(self, request, call_next):
        start_time = time.time()

        response: Response = await call_next(request)
        duration = time.time() - start_time
        logger.info(
            f"{request.client.host} - \"{request.method.upper()} {request.url} HTTP/{request.scope.get('http_version', 'unknown')}\" - {response.status_code} - T{duration:.2f}s"
        )

        return response
