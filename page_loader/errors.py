from page_loader.logger import page_loader_logger
import sys
from typing import Type

logger = page_loader_logger


def make_error(err_type: Type[Exception],
               msg: str) -> None:
    try:
        raise err_type(msg)
    except err_type:
        logger.error(sys.exc_info()[1])
        raise
