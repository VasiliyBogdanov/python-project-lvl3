from page_loader.error_handler import check_directory
from page_loader.logger import page_loader_logger
from page_loader.processors import (download_resources,
                                    parse_resources,
                                    save_page,
                                    )

logger = page_loader_logger


def download(url: str, directory: str = None) -> str:
    """Downloads webpage with its local resources
     inside 'img', 'link' and 'script' tags.

    Args:
        url: webpage url to download
        directory: directory to save webpage .html file with its resources.
            For resource files new folder will be created with '_files' suffix
             inside this directory.
    Return:
        Filepath to downloaded .html file in str format.
    Raises:
        (requests.ConnectionError
        requests.HTTPError
        requests.Timeout): subclasses of IOError.
        OSError: directory param does not exist.
        PermissionError: you don't have necessary rights to write to directory.
    """
    directory = check_directory(directory)
    html_content, download_links = parse_resources(url)
    download_resources(url, directory, download_links)
    html_path = save_page(html_content, url, directory)
    return html_path
