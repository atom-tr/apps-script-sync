from datetime import datetime
from logging import getLogger, Logger, StreamHandler
from string import Template
from typing import Dict

from humanize import precisedelta


class Logger:
    _COLOR_RESET = "\u001B[0m"
    _COLOR_RED = "\u001B[31m"
    _COLOR_GREEN = "\u001B[32m"
    _COLOR_BLUE = "\u001B[34m"
    _COLOR_YELLOW = "\u001B[33m"

    _DATE_TEMPLATE = "date"
    _TIME_TEMPLATE = "time"

    _logger: Logger

    def __init__(self, level: str):
        self._logger = getLogger(__name__)
        self._logger.setLevel(level)
        self._logger.addHandler(StreamHandler())

    @classmethod
    def _process_template(cls, message: str, kwargs: Dict) -> str:
        if cls._DATE_TEMPLATE in kwargs:
            kwargs[cls._DATE_TEMPLATE] = f"{datetime.strftime(kwargs[cls._DATE_TEMPLATE], '%d-%m-%Y %H:%M:%S:%f')}"
        if cls._TIME_TEMPLATE in kwargs:
            kwargs[cls._TIME_TEMPLATE] = precisedelta(kwargs[cls._TIME_TEMPLATE], minimum_unit="microseconds")

        return Template(message).substitute(kwargs)

    @classmethod
    def g(cls, message: str, **kwargs):
        message = cls._process_template(message, kwargs)
        cls._logger.info(f"{cls._COLOR_GREEN}{message}{cls._COLOR_RESET}")

    @classmethod
    def i(cls, message: str, **kwargs):
        message = cls._process_template(message, kwargs)
        cls._logger.debug(f"{cls._COLOR_BLUE}{message}{cls._COLOR_RESET}")

    @classmethod
    def w(cls, message: str, **kwargs):
        message = cls._process_template(message, kwargs)
        cls._logger.warning(f"{cls._COLOR_YELLOW}{message}{cls._COLOR_RESET}")

    @classmethod
    def p(cls, message: str, **kwargs):
        message = cls._process_template(message, kwargs)
        cls._logger.error(message)
