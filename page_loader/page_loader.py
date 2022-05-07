from bs4 import BeautifulSoup
from page_loader.logger import page_loader_logger
import os
from page_loader.formatters import format_filename
from page_loader.tag_processors import process_tags
import pathlib
import requests

logger = page_loader_logger


def download(url: str, directory: str = None, *, log: bool = False) -> str:
    if not log:
        logger.disabled = True
    if directory is None:
        directory = os.getcwd()
    if not pathlib.Path(directory).exists():
        raise OSError("Directory does not exist")

    session = requests.Session()
    content = session.get(url).text

    html_path = os.path.join(directory, format_filename(url, ext='.html'))
    files_folder_name = format_filename(url, ext='_files')
    files_path = os.path.join(directory, files_folder_name)

    # Create directory for downloaded files
    if not pathlib.Path(files_path).exists():
        os.mkdir(files_path)

    # Parse html for img tags
    soup = BeautifulSoup(content, 'html.parser')
    resource_tags = soup.find_all(['img', 'link', 'script'])

    process_tags(resource_tags, session, url, files_path, files_folder_name)

    with open(html_path, mode='w') as output_html:
        output_html.write(soup.prettify())

    return html_path
