from loguru import logger

from config import Config


def setup_logger():
    logger.add("logs/logs.log", format="{time} {level} {message}", rotation="10:00", compression="zip")
