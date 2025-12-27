from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.endpoints import llm, stt, tts
from .middlewares.logging import LoggingMiddleware
from .middlewares.metrics import (  # Import MetricsMiddleware class and metrics_endpoint function
    MetricsMiddleware,
    metrics_endpoint,
)
from .middlewares.rate_limiter import initialize_rate_limiter

load_dotenv()  # Load environment variables from .env file

app = FastAPI(
    title="Local Voice Assistant API",
    description="API for Japanese Speech-to-Text and LLM services.",
    version="1.0.0",
    on_startup=[initialize_rate_limiter],  # Initialize rate limiter on startup
)

origins = [
    "http://localhost:3000",  # Allow frontend during development
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


app.include_router(stt.router, prefix="/api/v1", tags=["stt"])
app.include_router(llm.router, prefix="/api/v1/llm", tags=["llm"])
app.include_router(tts.router, prefix="/api/v1/tts", tags=["tts"])
