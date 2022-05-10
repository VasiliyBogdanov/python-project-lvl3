from bs4 import BeautifulSoup
import os
from page_loader.logger import page_loader_logger
from page_loader.error_handler import make_error
from page_loader.formatters import format_filename
from page_loader.tag_processors import process_tags
import pathlib
import requests
from requests import ConnectionError
import sys

logger = page_loader_logger


def download(url: str, directory: str = None, *, log: bool = False,
             logger=logger) -> str:
    if not pathlib.Path(directory).exists():
        make_error(OSError,
                   f'Directory \'{directory}\' does not exist',
                   logger)

    if directory is None:
        directory = os.getcwd()
    elif not os.access(directory, mode=os.W_OK):
        make_error(PermissionError,
                   f'You don\'t have rights to write to {directory}',
                   logger)

    if not log:
        logger.disabled = True

    session = requests.Session()

    try:
        content = session.get(url).text
    except ConnectionError:
        logger.error(sys.exc_info()[1])
        raise

    html_path = os.path.join(directory, format_filename(url, ext='.html'))
    files_folder_name = format_filename(url, ext='_files')
    files_path = os.path.join(directory, files_folder_name)

    # Create directory for downloaded files
    if not pathlib.Path(files_path).exists():
        os.mkdir(files_path)

    # Parse html for img tags
    soup = BeautifulSoup(content, 'html.parser')
    resource_tags = soup.find_all(['img', 'link', 'script'])

    process_tags(resource_tags, session, url, files_path, files_folder_name,
                 logger)

    with open(html_path, mode='w') as output_html:
        output_html.write(soup.prettify())

    return html_path
