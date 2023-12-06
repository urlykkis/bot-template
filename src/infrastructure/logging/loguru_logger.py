"""Логирование"""
from typing import List

import logging

from loguru import logger

from src.domain.enums.log_level import LogLevel


log_levels = [LogLevel.INFO, LogLevel.ERROR, LogLevel.DEBUG]
log_format = "{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message}"


for level in log_levels:
    logger.add(
        f"./logs/{level.name.lower()}.log",
        level=level.name, colorize=False,
        format=log_format, rotation="10 MB",
        compression="zip",
    )


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logger(level: LogLevel = LogLevel.INFO, ignored: List[str] = []):
    """
    Устанавливает логирование на определенном уровне
    Убирает ненужные группы логов
    """
    logging.basicConfig(handlers=[InterceptHandler()], level=level)

    for name in ["aiogram.middlewares", "aiogram.event", "aiohttp.access"]:
        logging.getLogger(name).setLevel(logging.WARNING)

    for ignore in ignored:
        logger.disable(ignore)
