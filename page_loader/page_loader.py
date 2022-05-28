from page_loader.downloaders import (download_page,
                                     download_resources,
                                     )
from page_loader.logger import page_loader_logger
from page_loader.parsers import parse_resources
from page_loader.paths import check_directory
from page_loader.savers import save_page

logger = page_loader_logger


def download(url: str, directory: str = None) -> str:
    """Downloads webpage with its local resources
     inside 'img', 'link' and 'script' tags.

     :param url: webpage url to download
     :param directory: directory to save webpage .html file with its resources.
            For resource files new folder will be created with '_files' suffix
             inside this directory.
    :return: Filepath to downloaded .html file in str format.
    :raise requests.ConnectionError: subclass of IOError.
    :raise requests.HTTPError: subclass of IOError.
    :raise requests.Timeout: subclass of IOError.
    :raise OSError: directory param does not exist.
    :raise PermissionError: you don't have necessary rights
     to write to directory.
    """
    directory = check_directory(directory)
    content = download_page(url)
    html_content, download_links = parse_resources(content, directory)
    download_resources(url, directory, download_links)
    html_path = save_page(html_content, url, directory)
    return html_path
