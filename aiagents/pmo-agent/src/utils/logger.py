"""Logging configuration for PMO Agent."""
import logging
from src.config import settings


def configure_logging():
    """Configure logging for the application."""
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('pmo_agent.log'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)
