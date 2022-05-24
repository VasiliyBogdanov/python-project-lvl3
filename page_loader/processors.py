from bs4 import BeautifulSoup
from collections import namedtuple
import os
from page_loader.error_handler import (download_page,
                                       download_tag,
                                       HTML_SUFFIX)
from page_loader.formatters import (format_filename,
                                    format_host_name)
from pathlib import Path
from progress.bar import Bar
from typing import Tuple
from urllib.parse import (urljoin, urlparse)

TAG_LINKS = {
    'img': 'src',
    'link': 'href',
    'script': 'src'
}
_TAG_NAMES = namedtuple('Tag_names', 'img link script')
TAG_NAMES = _TAG_NAMES('img', 'link', 'script')
FILES_FOLDER_SUFFIX = '_files'
SOUP_PARSER = 'html.parser'


def save_page(html: str,
              url: str,
              directory: str) -> str:
    """Saves downloaded webpage with modified links,
     so they point to downloaded resources.

    Args:
        html: 'Prettified' html file
        url: webpage url to download
        directory: directory to save webpage .html file with its resources.
            For resource files new folder will be created with
             '_files' suffix inside this directory.
    Returns:
        Path to saved html file.
    """
    html_path = Path().joinpath(directory,
                                format_host_name(url) + HTML_SUFFIX)

    with open(html_path, mode='w') as output_html:
        output_html.write(html)

    return str(html_path)


def make_modified_path(home_url: str,
                       tag_url: str) -> str:
    host = urlparse(home_url).netloc
    left_side = format_host_name(home_url) + FILES_FOLDER_SUFFIX
    path, ext = os.path.splitext(tag_url)
    path = path[1:] if path.startswith('/') else path
    ext = ext if ext else HTML_SUFFIX

    if urlparse(path).scheme:
        right_side = format_filename(path) + ext
    else:
        right_side = format_host_name(os.path.join(format_host_name(host),
                                                   path)) + ext
    return os.path.join(left_side, right_side)


def make_path_to_download(home_url: str,
                          tag_url: str) -> str:
    home_url = home_url if home_url.endswith('/') else home_url + '/'
    return urljoin(home_url, tag_url)


def is_absolute_path(url: str,
                     link: str) -> bool:
    parsed_url = urlparse(url)
    parsed_tag = urlparse(link)
    if parsed_tag.scheme and parsed_tag.netloc == parsed_url.netloc:
        return True
    return False


def is_external_link(home_url: str,
                     link: str) -> bool:
    """If False, link is considered internal."""
    parsed_tag = urlparse(link)
    if is_absolute_path(home_url, link) or \
            not parsed_tag.scheme:
        return False
    return True


def save_data(data: bytes,
              path: os.PathLike) -> None:
    """Wrapper for saving data."""
    with open(path, mode='wb') as f:
        f.write(data)


def download_resources(url: str,
                       directory: str,
                       download_links: list) -> None:
    """Downloads resources.

    Args:
        url: webpage url to download
        directory: directory to save webpage .html file with its resources.
            For resource files new folder will be created with
             '_files' suffix inside this directory.
        download_links: links to download.
    """
    if not download_links:
        return

    make_assets_directory(url, directory)
    bar = Bar(max=len(download_links))

    for link in download_links:
        if is_absolute_path(url, link):
            file_to_save = link
        else:
            file_to_save = make_path_to_download(url, link)

        filepath_to_save = Path\
            .joinpath(Path(directory),
                      Path(make_modified_path(url,
                                              link)))

        data = download_tag(file_to_save, bar)
        save_data(data.content, filepath_to_save)

    bar.finish()


def parse_resources(url: str) -> Tuple[str, list]:
    """Downloads webpage, parses its tags, saves links
     to files (that are local to webpage)
    and modifies paths inside downloaded .html
     to point to downloaded resources.

    Args:
        url: webpage url to download.
    Returns:
        'Prettified' html, links to resources.
    """
    content = download_page(url)
    soup = BeautifulSoup(content, SOUP_PARSER)
    tags = soup.find_all([TAG_NAMES.img,
                          TAG_NAMES.link,
                          TAG_NAMES.script])

    download_links = []
    for tag in tags:
        if tag.get(TAG_LINKS[tag.name]) is None or\
                is_external_link(url, tag[TAG_LINKS[tag.name]]):
            continue

        download_links.append(tag[TAG_LINKS[tag.name]])

        modified_path = make_modified_path(url, tag[TAG_LINKS[tag.name]])
        tag[TAG_LINKS[tag.name]] = modified_path

    return soup.prettify(), download_links


def make_assets_directory(url: str,
                          directory: str) -> None:
    files_folder_name = format_host_name(url) + FILES_FOLDER_SUFFIX
    files_path = Path().joinpath(directory, files_folder_name)

    Path.mkdir(files_path, exist_ok=True)
