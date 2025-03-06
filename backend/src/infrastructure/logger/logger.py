import logging

from src.domain.abstractions.logger.logger import AbstractLogger


class Logger(AbstractLogger):
    def __init__(self, log_file: str = "app.log"):
        self.logger = logging.getLogger("application_log")
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def warning(self, message: str):
        self.logger.warning(message)
