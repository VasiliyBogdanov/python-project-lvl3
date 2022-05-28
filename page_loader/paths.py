import os
from page_loader.errors import (HTML_SUFFIX,
                                make_error)
from page_loader.formatters import (format_filename,
                                    format_host_name,
                                    )
from pathlib import Path
import requests
from urllib.parse import (urljoin,
                          urlparse)

TAG_LINKS = {
    'img': 'src',
    'link': 'href',
    'script': 'src'
}
FILES_FOLDER_SUFFIX = '_files'


def check_directory(directory: str) -> str:
    if not Path(directory).exists():
        make_error(OSError,
                   f'Directory \'{directory}\' does not exist')

    if directory is None:
        directory = os.getcwd()
    elif not os.access(directory, mode=os.W_OK):
        make_error(PermissionError,
                   f'You don\'t have rights to write to {directory}')
    return directory


def is_absolute_path(url: str,
                     link: str) -> bool:
    parsed_url = urlparse(url)
    parsed_tag = urlparse(link)
    if parsed_tag.scheme and parsed_tag.netloc == parsed_url.netloc:
        return True
    return False


def is_external_link(home_url: str,
                     link: str) -> bool:
    parsed_tag = urlparse(link)
    if is_absolute_path(home_url, link) or \
            not parsed_tag.scheme:
        return False
    return True


def make_assets_directory(url: str,
                          directory: str) -> None:
    files_folder_name = format_host_name(url) + FILES_FOLDER_SUFFIX
    files_path = Path().joinpath(directory, files_folder_name)

    Path.mkdir(files_path, exist_ok=True)


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


def make_path_to_resource(content: requests.Response,
                          directory: str,
                          tag) -> Path:
    filepath_to_save = Path \
        .joinpath(Path(directory),
                  Path(make_modified_path(
                      content.url,
                      tag[TAG_LINKS[tag.name]])))
    return filepath_to_save
