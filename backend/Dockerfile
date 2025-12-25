FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency file
COPY requirements.in .

# Install dependencies into a virtual environment
RUN uv venv --python 3.11
RUN . .venv/bin/activate && uv pip install -r requirements.in

# Copy source code
COPY . .

# Pre-download the model (Optional but recommended for faster startup)
# This requires a script or command that triggers the model download
# For now, we'll assume the model is downloaded on first use as per quickstart.
# RUN . .venv/bin/activate && python -c "from src.core.stt_processor import stt_processor; stt_processor._load_model_if_needed()"

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app/src
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

# Run the application
CMD [".venv/bin/python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
