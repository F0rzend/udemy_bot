from loguru import logger

from .errors import retry_after
from .private import deeplinks, start, referral_codes

logger.info("Handlers are successfully configured")
