import logging
from page_loader.logger import page_loader_logger
from requests import HTTPError, ConnectionError
import requests
import sys
from typing import Type

logger = page_loader_logger


def make_error(err_type: Type[Exception],
               msg: str,
               logger: logging.Logger) -> None:
    try:
        raise err_type(msg)
    except err_type:
        logger.error(sys.exc_info()[1])
        raise


def try_to_download_tag(session: requests.Session,
                        download_path,
                        logger, bar) -> requests.Response:
    try:
        data_to_save = session.get(download_path, stream=True)
        data_to_save.raise_for_status()
    except (HTTPError, ConnectionError):
        logger.error(sys.exc_info()[1])
        raise
    else:
        bar.next()
        logger.info(f'{data_to_save.status_code} '
                    f'{data_to_save.reason} '
                    f'{download_path}')

        return data_to_save


def try_to_download_page(session: requests.Session,
                         url: str) -> requests.Response.text:
    try:
        content = session.get(url)
        content.raise_for_status()
    except (HTTPError, ConnectionError):
        logger.error(sys.exc_info()[1])
        raise
    else:
        return content.text
