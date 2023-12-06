class LoggerAdapter:
    def __init__(self, default_logger):
        self.default_logger = default_logger

    def info(self, *args, **kwargs):
        return self.default_logger.info(*args, **kwargs)

    def debug(self, *args, **kwargs):
        return self.default_logger.debug(*args, **kwargs)

    def error(self, *args, **kwargs):
        return self.default_logger.error(*args, **kwargs)
