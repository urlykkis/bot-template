from .loguru_logger import logger as loguru_logger, setup_logger
from .adapter import LoggerAdapter


logger = LoggerAdapter(default_logger=loguru_logger)
