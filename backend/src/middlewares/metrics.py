import time

from prometheus_client import Counter, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status_code"]
)
REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds", "HTTP request duration in seconds", ["method", "endpoint"]
)

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method = request.method
        endpoint = request.url.path # Simplified endpoint for now

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        status_code = response.status_code

        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status_code=status_code).inc()
        REQUEST_DURATION_SECONDS.labels(method=method, endpoint=endpoint).observe(process_time)

        return response

def metrics_endpoint(request: Request):
    """Exposes Prometheus metrics at /metrics endpoint.
    """
    return Response(content=generate_latest(), media_type="text/plain")
