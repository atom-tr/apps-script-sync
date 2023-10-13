from datetime import datetime
from logging import getLogger, Logger, StreamHandler
from string import Template
from typing import Dict

from humanize import precisedelta


class Logger:
    _RESET = "\u001B[0m"
    _RED = "\u001B[31m"
    _GREEN = "\u001B[32m"
    _BLUE = "\u001B[34m"
    _YELLOW = "\u001B[33m"

    _DATE_TEMPLATE = "date"
    _TIME_TEMPLATE = "time"

    _logger: Logger

    def __init__(self, level: str):
        self._logger = getLogger(__name__)
        self._logger.setLevel(level)
        self._logger.addHandler(StreamHandler())

    def _process_template(self, message: str, kwargs: Dict) -> str:
        if self._DATE_TEMPLATE in kwargs:
            kwargs[self._DATE_TEMPLATE] = f"{datetime.strftime(kwargs[self._DATE_TEMPLATE], '%d-%m-%Y %H:%M:%S:%f')}"
        if self._TIME_TEMPLATE in kwargs:
            kwargs[self._TIME_TEMPLATE] = precisedelta(kwargs[self._TIME_TEMPLATE], minimum_unit="microseconds")

        return Template(message).substitute(kwargs)

    def g(self, message: str, **kwargs):
        message = self._process_template(message, kwargs)
        self._logger.info(f"{self._GREEN}{message}{self._RESET}")

    def i(self, message: str, **kwargs):
        message = self._process_template(message, kwargs)
        self._logger.debug(f"{self._BLUE}{message}{self._RESET}")

    def w(self, message: str, **kwargs):
        message = self._process_template(message, kwargs)
        self._logger.warning(f"{self._YELLOW}{message}{self._RESET}")

    def p(self, message: str, **kwargs):
        message = self._process_template(message, kwargs)
        self._logger.error(message)
