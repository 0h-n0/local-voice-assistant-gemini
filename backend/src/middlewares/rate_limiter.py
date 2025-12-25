from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from redis.asyncio import Redis
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import os

# Initialize Redis client (replace with actual Redis URL if not localhost)
redis_client: Redis = Redis(host=os.getenv("REDIS_HOST", "localhost"), port=int(os.getenv("REDIS_PORT", 6379)), db=0, encoding="utf-8", decode_responses=True)

async def initialize_rate_limiter():
    """Initializes the FastAPI-Limiter."""
    await FastAPILimiter.init(redis_client)

async def get_client_id(request: Request):
    """
    Identifies the client for rate limiting.
    Uses API Key if present, otherwise falls back to client IP.
    """
    api_key = request.headers.get("X-API-Key") or request.query_params.get("api_key")
    if api_key:
        return api_key
    return request.client.host # Fallback to IP address if no API key

# Define default rate limit
DEFAULT_RATE_LIMIT = "60/minute" # 60 requests per minute

# Middleware to apply rate limiting. 
# This is a placeholder; actual application would involve
# `@limiter.limit` decorators on specific routes.
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, default_limit: str = DEFAULT_RATE_LIMIT):
        super().__init__(app)
        self.default_limit = default_limit

    async def dispatch(self, request: Request, call_next):
        # This middleware only initializes FastAPILimiter.
        # Actual rate limiting is applied via dependencies on routes.
        # This is a basic setup. For per-route specific limits,
        # use @limiter.limit("rate/interval") in your endpoint.
        try:
            # We don't apply a global limit here, but ensure FastAPILimiter is ready
            # The RateLimiter dependency will be used on individual routes.
            pass
        except HTTPException as e:
            if e.status_code == 429:
                return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)
            raise # Re-raise other HTTPExceptions
        return await call_next(request)

# Dependency for applying rate limit to a route
# Example usage: @router.post("/my-endpoint", dependencies=[Depends(rate_limit_dependency)])
rate_limit_dependency = RateLimiter(times=int(DEFAULT_RATE_LIMIT.split('/')[0]), 
                                     minutes=int(DEFAULT_RATE_LIMIT.split('/')[1].replace('minute', '1')))
