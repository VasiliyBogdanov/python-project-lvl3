import sys
from pathlib import Path

import requests
from progress.bar import Bar
from requests import (ConnectionError,
                      HTTPError,
                      Timeout,
                      )

from page_loader.logger import page_loader_logger
from page_loader.paths import (is_absolute_path,
                               make_assets_directory,
                               make_path_to_download,
                               )
from page_loader.savers import save_data

logger = page_loader_logger


def download_page(url: str) -> requests.Response:
    try:
        content = requests.get(url)
        content.raise_for_status()
    except (HTTPError, ConnectionError):
        logger.error(sys.exc_info()[1])
        raise
    else:
        return content


def download_resources(url: str,
                       directory: str,
                       download_links: list) -> None:
    """Downloads and saves resources.

    :param url: webpage url to download
    :param directory: directory to save webpage .html file with its resources.
            For resource files new folder will be created with
             '_files' suffix inside this directory.
    :param download_links: links to download.
    """
    if not download_links:
        return

    make_assets_directory(url, directory)
    bar = Bar(max=len(download_links))

    for link, download_path in download_links:
        if is_absolute_path(url, link):
            file_to_save = link
        else:
            file_to_save = make_path_to_download(url, link)
        bar.next()
        data = download_tag(file_to_save)
        save_data(data.content, download_path)

    bar.finish()


def download_tag(download_path: Path) -> requests.Response:
    try:
        data_to_save = requests.get(download_path)
        data_to_save.raise_for_status()
    except (HTTPError, ConnectionError, Timeout):
        logger.error(sys.exc_info()[1])
        raise
    else:
        logger.info(f'{data_to_save.status_code} '
                    f'{data_to_save.reason} '
                    f'{download_path}')

        return data_to_save
