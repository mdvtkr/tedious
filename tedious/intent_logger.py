import logging
from rich.logging import RichHandler
from rich.console import Console

def get(name, format="[%(name)-20s] %(message)s", level=logging.DEBUG):
    logger = logging.getLogger(name)
    formatter = logging.Formatter(format)
    handler = RichHandler(rich_tracebacks=True, console=Console(width=150))
    handler.setFormatter(formatter)
    logger.handlers = [handler]
    logger.setLevel(level)

    info = lambda x, indent=0: logger.info("  "*indent + str(x).replace('\n', '\n'+"  "*indent))
    dbg = lambda x, indent=0: logger.debug("  "*indent + str(x).replace('\n', '\n'+"  "*indent))
    err = lambda x, indent=0: logger.error("  "*indent + str(x).replace('\n', '\n'+"  "*indent))
    return info, dbg, err, logger