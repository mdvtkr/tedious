import logging
from rich.logging import RichHandler
from rich.console import Console
from enum import Enum
from logging.handlers import RotatingFileHandler

class FORMAT(str, Enum):
    NAME_MESSAGE = "[%(name)s] %(message)s"
    NAME_THREAD_MESSAGE = "[%(name)s][%(threadName)s] %(message)s"

def conv_level_code(level:str):
    if level == "info":
        level = logging.INFO
    elif level == "debug":
        level = logging.DEBUG
    elif level == "error":
        level = logging.ERROR
    elif level == "fatal":
        level = logging.CRITICAL    
    elif level == "warn":
        level = logging.WARN
    elif type(level) == str:
        level = logging.INFO
    return level


def get(name, format:FORMAT|str=FORMAT.NAME_MESSAGE, level=logging.DEBUG, file=None):
    logger = logging.getLogger(name)
    formatter = logging.Formatter(format)
    handler = RichHandler(rich_tracebacks=True, console=Console(width=150))
    handler.setFormatter(formatter)
    handlers = [handler]

    if file:
        from pathlib import Path
        Path(file).parent.mkdir(0o755, True, True)
        fileHandler = RotatingFileHandler(file, 
                                          mode='a', 
                                          maxBytes=1024 * 1024 * 10,  # 10Mb
                                          backupCount=3)
        fileHandler.setFormatter(formatter)
        handlers.append(fileHandler)
    logger.handlers = handlers

    logger.setLevel(conv_level_code(level))

    info = lambda x, indent=0: logger.info("  "*indent + str(x).replace('\n', '\n'+"  "*indent), stacklevel=2)
    dbg = lambda x, indent=0: logger.debug("  "*indent + str(x).replace('\n', '\n'+"  "*indent), stacklevel=2)
    err = lambda x, indent=0: logger.error("  "*indent + str(x).replace('\n', '\n'+"  "*indent), stacklevel=2)
    return info, dbg, err, logger