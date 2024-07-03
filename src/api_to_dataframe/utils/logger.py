import logging
from enum import Enum


class LogLevel(Enum):
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR


# Configure logging once at the start of your program
logging.basicConfig(
    encoding="utf-8",
    format="%(asctime)s :: %(levelname)s :: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %Z",
    level=logging.DEBUG,
)


def log(message: str, level: LogLevel):
    logger = logging.getLogger("api-to-dataframe")
    logger.log(level.value, message)


log("This is an info message", LogLevel.INFO)
log("This is a warning message", LogLevel.WARNING)
log("This is an error message", LogLevel.ERROR)
