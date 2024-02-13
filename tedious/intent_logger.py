
import logging
from rich.logging import RichHandler

def get(name, format="%(message)s", level="NOTSET"):
    logger = logging.getLogger(name)
    formatter = logging.Formatter(format)
    handler = RichHandler(rich_tracebacks=True)
    handler.setFormatter(formatter)
    logging.basicConfig(
        level=level, 
        handlers=[handler]
    )

    info = lambda x, indent=0: logger.info("  "*indent + str(x).replace('\n', '\n'+"  "*indent))
    dbg = lambda x, indent=0: logger.debug("  "*indent + str(x).replace('\n', '\n'+"  "*indent))
    err = lambda x, indent=0: logger.error("  "*indent + str(x).replace('\n', '\n'+"  "*indent))
    return info, dbg, err