import logging
import time

from pythonjsonlogger import jsonlogger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# Configure JSON logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    fmt='%(levelname)s %(asctime)s %(name)s %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        log_dict = {
            "request_id": request.headers.get("X-Request-ID"), # Assuming a request ID is passed
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "process_time": f"{process_time:.4f}s",
            "client_ip": request.client.host if request.client else "unknown",
            # Add more relevant info as needed, e.g., audio length for STT endpoints
        }

        logger.info("HTTP Request", extra=log_dict)
        return response
