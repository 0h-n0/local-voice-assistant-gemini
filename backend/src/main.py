from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from .middlewares.logging import LoggingMiddleware
from .middlewares.metrics import MetricsMiddleware, metrics_endpoint # Import MetricsMiddleware class and metrics_endpoint function
from .middlewares.rate_limiter import RateLimitMiddleware, initialize_rate_limiter
from .api.v1.endpoints import stt

load_dotenv() # Load environment variables from .env file

app = FastAPI(
    title="Japanese STT API",
    description="API for Japanese Speech-to-Text transcription.",
    version="1.0.0",
    on_startup=[initialize_rate_limiter] # Initialize rate limiter on startup
)

origins = [
    "http://localhost:3000", # Allow frontend during development
    # Add other allowed origins in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(MetricsMiddleware)
# Prometheus metrics endpoint
app.add_route("/metrics", metrics_endpoint)


app.include_router(stt.router, prefix="/api/v1")
