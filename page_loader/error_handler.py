import os
from page_loader.progress import bar
from page_loader.logger import page_loader_logger
from pathlib import Path
import requests
from requests import HTTPError, ConnectionError
import sys
from typing import Tuple
from typing import Type

logger = page_loader_logger


def make_error(err_type: Type[Exception],
               msg: str) -> None:
    try:
        raise err_type(msg)
    except err_type:
        logger.error(sys.exc_info()[1])
        raise


def download_tag(download_path: Path) -> requests.Response:
    try:
        data_to_save = requests.get(download_path)
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


def download_page(url: str) -> str:
    try:
        content = requests.get(url)
        content.raise_for_status()
    except (HTTPError, ConnectionError):
        logger.error(sys.exc_info()[1])
        raise
    else:
        return content.text


def check_input(url: str,
                directory: str) -> Tuple[str, str]:
    if not Path(directory).exists():
        make_error(OSError,
                   f'Directory \'{directory}\' does not exist')

    if directory is None:
        directory = os.getcwd()
    elif not os.access(directory, mode=os.W_OK):
        make_error(PermissionError,
                   f'You don\'t have rights to write to {directory}')
    url = url.rstrip('/')
    return url, directory
