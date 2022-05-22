from bs4 import BeautifulSoup
from page_loader.error_handler import (check_input,
                                       download_page,
                                       )
from page_loader.logger import page_loader_logger
from page_loader.processors import (download_resources,
                                    make_directory,
                                    modify_html,
                                    parse_resources,
                                    save_page,
                                    )

logger = page_loader_logger


def download(url: str, directory: str = None) -> str:
    url, directory = check_input(url, directory)
    content = download_page(url)
    make_directory(url, directory)
    soup = BeautifulSoup(content, 'html.parser')

    download_links = parse_resources(url, soup)
    download_resources(url, directory, download_links)
    page = modify_html(url, directory, download_links)
    save_page(soup.prettify(), url, directory)
    return page
