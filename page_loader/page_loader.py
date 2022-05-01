from bs4 import BeautifulSoup
from collections import namedtuple
from page_loader.formatters import format_filename
from page_loader.downloaders import download_resources
import os
import pathlib
import requests


def download(url: str, directory: str = None) -> str:
    if directory is None:
        directory = os.getcwd()
    if not pathlib.Path(directory).exists():
        raise OSError("Directory does not exist")

    content = requests.get(url).text

    html_path = os.path.join(directory, format_filename(url, ext='.html'))
    files_suffix = format_filename(url, ext='_files')
    files_path = os.path.join(directory, files_suffix)

    # Create directory for downloaded files
    if not pathlib.Path(files_path).exists():
        os.mkdir(files_path)

    # Parse html for img tags
    soup = BeautifulSoup(content, 'html.parser')
    images = soup.find_all('img', recursive=True)
    links = soup.find_all('link', recursive=True)
    scripts = soup.find_all('script', recursive=True)

    _resources = namedtuple('Resources', 'images links scripts')
    resources = _resources(images, links, scripts)

    session = requests.Session()

    # Download AND modify html
    download_resources(session, resources, url, files_path)

    # Save modified html
    with open(html_path, mode='w') as output_html:
        output_html.write(soup.prettify())

    return html_path
