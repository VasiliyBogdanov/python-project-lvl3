from page_loader.error_handler import check_input
from page_loader.error_handler import download_page
from page_loader.logger import page_loader_logger
from page_loader.processors import make_directory
from page_loader.processors import process_resources

logger = page_loader_logger


def download(url: str, directory: str = None) -> str:
    url, directory = check_input(url, directory)

    content = download_page(url)

    make_directory(url, directory)
    html_path = process_resources(content, url, directory)

    return str(html_path)
