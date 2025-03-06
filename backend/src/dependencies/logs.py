from fastapi import Depends

from src.domain.abstractions.logger.logger import AbstractLogger
from src.infrastructure.logger.logger import Logger
from src.services.logs.log import LogService


class LogDependencies:
    @staticmethod
    def get_logger() -> AbstractLogger:
        return Logger()

    @staticmethod
    def get_log_service(
            logger: AbstractLogger = Depends(get_logger)
    ) -> LogService:
        return LogService(logger)
