import logging

from bs4 import BeautifulSoup
import os
from page_loader.error_handler import make_error
from page_loader.error_handler import try_to_download_page
from page_loader.formatters import format_host_name
from page_loader.logger import page_loader_logger
import page_loader.K as K
from page_loader.processors import process_tags
from page_loader.processors import prepare_resources
from pathlib import Path
from progress.bar import Bar
import requests


logger = page_loader_logger


def download(url: str, directory: str = None, *, log: bool = False,
             logger: logging.Logger = logger) -> str:
    if not log:
        logger.disabled = True

    if not Path(directory).exists():
        make_error(OSError,
                   f'Directory \'{directory}\' does not exist',
                   logger)

    if directory is None:
        directory = os.getcwd()
    elif not os.access(directory, mode=os.W_OK):
        make_error(PermissionError,
                   f'You don\'t have rights to write to {directory}',
                   logger)

    session = requests.Session()
    url = url.rstrip('/')

    content = try_to_download_page(session, url)

    html_path = Path().joinpath(directory,
                                format_host_name(url) + K.HTML_SUFFIX)
    files_folder_name = format_host_name(url) + K.FILES_FOLDER_SUFFIX
    files_path = Path().joinpath(directory, files_folder_name)

    Path.mkdir(files_path, exist_ok=True)

    soup = BeautifulSoup(content, 'html.parser')
    resource_tags, resource_len = prepare_resources(soup, url)

    bar = Bar(max=resource_len)

    process_tags(resource_tags, session, url, directory,
                 logger, bar)

    with open(html_path, mode='w') as output_html:
        output_html.write(soup.prettify())

    bar.finish()

    return str(html_path)
