"""Logging utilities."""
import logging
import sys

from pythonjsonlogger import jsonlogger


def setup_logger(name: str):
    """Set up a JSON logger with the given name."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = jsonlogger.JsonFormatter(
            fmt='%(levelname)s %(asctime)s %(name)s %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

llm_logger = setup_logger("llm_service")

def log_llm_usage(model: str, prompt_tokens: int, completion_tokens: int, total_tokens: int, request_id: str = None):
    """Log LLM token usage information."""
    llm_logger.info("LLM Usage", extra={
        "llm_model": model,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "request_id": request_id
    })
