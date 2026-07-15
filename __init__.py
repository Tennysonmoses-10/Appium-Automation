"""Partner App QA Framework - Package initialization."""

from core.logger import logger, setup_logging
from config.settings import settings

# Initialize logging
setup_logging()

__version__ = "1.0.0"
__author__ = "QA Automation Team"
__email__ = "qa@partnerapp.com"

logger.info(f"Partner App QA Framework v{__version__}")
logger.info(f"Environment: {settings.environment}")
logger.info(f"Log Level: {settings.log_level}")
