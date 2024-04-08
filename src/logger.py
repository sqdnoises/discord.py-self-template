from datetime import datetime
from typing import Callable, Any, Literal

from config import BOT_NAME, LOGGER_TIME_FORMAT 
from termcolors import *

__all__ = (
    "Logger",
)

color_log_types = {
    "info":  bold + blue,
    "warn":  bold + yellow,
    "error": bold + red,
    "fatal": bg_red,
    "debug": bold + bg_black
}

class Logger:
    """
    #### Log Levels:
    `0` - nothing

    `1` - info
    
    `2` - warning
    
    `3` - error
    
    `4` - critical
    
    `5` - debug
    """

    def __init__(self, name: str = BOT_NAME, prefix: Callable[[str], str] | None = None, log_level: int = 4, color_log_types: dict[str, str] = color_log_types) -> None:
        self.name = str(name)
        self._prefix = prefix
        self.log_level = log_level
        self._log_colors = color_log_types

        if self._prefix is None:
            self._prefix = self._prefix_handler

    def log(self, log_type: Literal["info", "warning", "error", "critical", "debug"], message: Any) -> None:
        if log_type == "info":
            log_level = 1
        elif log_type == "warning":
            log_level = 2
        elif log_type == "error":
            log_level = 3
        elif log_type == "fatal":
            log_level = 4
        else:
            log_level = 5

        if log_level <= self.log_level:
            prefix = str(self._prefix(log_type))
            print(prefix + message, end=reset+"\n")
    
    def info(self, message: str | Any) -> None:
        self.log("info", message)
    
    def warn(self, message: str | Any) -> None:
        self.warn("warning", message)
    
    def warning(self, message: str | Any) -> None:
        self.log("warning", message)
    
    def error(self, message: str | Any) -> None:
        self.log("error", message)
    
    def critical(self, message: str | Any) -> None:
        self.log("critical", message)
    
    def debug(self, message: str | Any) -> None:
        self.log("debug", message)
    
    def _prefix_handler(self, log_type: str) -> str:
        return f"{reset}{bold}{black}{datetime.now().strftime(LOGGER_TIME_FORMAT)}{reset} {bold}" + self._log_colors.get(log_type, reset) + "{:<8}".format(log_type.upper()) + f"{reset} {red}{self.name}{reset} "

logging = Logger()