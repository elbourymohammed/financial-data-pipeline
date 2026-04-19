import os
import logging
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Get log level from .env (default to INFO)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Configure basic logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
