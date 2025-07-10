"""Utils module for setting up a logger with rich formatting."""
#
# Imports
#

from rich.logging import RichHandler
from logging import Logger, basicConfig, getLogger

#
# Methods
#


def setup_logger(level: str = "INFO") -> Logger:
    if level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        raise ValueError(
            "Invalid logging level: %s. Available levels are: DEBUG, INFO, WARNING, ERROR, CRITICAL." % level
        )
    basicConfig(
        format="%(message)s",
        datefmt="[%X]",
        level=level,
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    logger: Logger = getLogger("rich")
    return logger

# intialize a static logger instance
static_logger: Logger = setup_logger()
