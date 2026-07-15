"""
Logging configuration for Partner App QA framework.
Provides structured logging with correlation IDs and contextual information.
"""

import logging
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4
from loguru import logger as loguru_logger
from config.settings import settings


class CorrelationIdFilter(logging.Filter):
    """Add correlation ID to all log records."""
    
    _correlation_id: str = str(uuid4())
    
    @classmethod
    def set_correlation_id(cls, correlation_id: str) -> None:
        """Set correlation ID for current context."""
        cls._correlation_id = correlation_id
    
    @classmethod
    def get_correlation_id(cls) -> str:
        """Get current correlation ID."""
        return cls._correlation_id
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Add correlation ID to record."""
        record.correlation_id = self._correlation_id
        record.request_id = str(uuid4())
        return True


class JSONFormatter(logging.Formatter):
    """Format logs as JSON for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": getattr(record, "correlation_id", "N/A"),
            "request_id": getattr(record, "request_id", "N/A"),
        }
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


def setup_logging() -> None:
    """Configure logging for the entire framework."""
    
    # Ensure logs directory exists
    settings.reporting.logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Remove default handlers
    loguru_logger.remove()
    
    # Configure loguru
    log_format = (
        "<level>{time:YYYY-MM-DD HH:mm:ss}</level> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    # Console handler
    if settings.enable_console_logging:
        loguru_logger.add(
            sys.stdout,
            format=log_format,
            level=settings.log_level,
            colorize=True,
        )
    
    # File handler
    log_file = settings.reporting.logs_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    loguru_logger.add(
        str(log_file),
        format=log_format,
        level=settings.log_level,
        rotation="500 MB",
        retention="7 days",
    )


def get_logger(name: str) -> Any:
    """Get logger instance with correlation ID filter."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.addFilter(CorrelationIdFilter())
        
        if settings.log_format == "json":
            formatter = JSONFormatter()
        else:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - [%(correlation_id)s] - %(message)s'
            )
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    logger.setLevel(getattr(logging, settings.log_level))
    return logger


# Initialize logging on module load
setup_logging()
logger = loguru_logger
