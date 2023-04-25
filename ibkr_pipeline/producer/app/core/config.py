import logging
import sys

from ibkr_pipeline.producer.app.core.logging1 import InterceptHandler
from loguru import logger
from starlette.config import Config

config = Config("../../../.env")


PROJECT_NAME: str = config("PROJECT_NAME", default="ibkr-kafka-producer")
KAFKA_URI: str = config("KAFKA_URI", default='0.0.0.0')
KAFKA_PORT: str = config("KAFKA_PORT", default='9092')
KAFKA_INSTANCE = KAFKA_URI + ":" + KAFKA_PORT
DEBUG: bool = config("DEBUG", cast=bool, default=False)

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO

logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])