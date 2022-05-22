import bs4
from page_loader.error_handler import download_tag, HTML_SUFFIX
from page_loader.formatters import (format_filename,
                                    format_host_name)
from pathlib import Path
from progress.bar import Bar
import os
from urllib.parse import (urljoin, urlparse)

TAG_LINKS = {
    'img': 'src',
    'link': 'href',
    'script': 'src'
}
FILES_FOLDER_SUFFIX = '_files'


def save_page(html: str,
              url: str,
              directory: str) -> None:
    html_path = Path().joinpath(directory,
                                format_host_name(url) + HTML_SUFFIX)

    with open(html_path, mode='w') as output_html:
        output_html.write(html)


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
                     tag: bs4.Tag,
                     tag_link_attr: str) -> bool:
    parsed_url = urlparse(url)
    parsed_tag = urlparse(tag[tag_link_attr])
    if parsed_tag.scheme and parsed_tag.netloc == parsed_url.netloc:
        return True
    return False


def is_external_link(home_url: str,
                     tag: bs4.Tag,
                     tag_link_attr: str) -> bool:
    """If False, link is considered internal."""
    parsed_tag = urlparse(tag[tag_link_attr])
    if is_absolute_path(home_url, tag, tag_link_attr) or \
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
                       tags: list) -> None:
    bar = Bar(max=len(tags))
    for tag in tags:
        if is_absolute_path(url, tag, TAG_LINKS[tag.name]):
            file_to_save = tag[TAG_LINKS[tag.name]]
        else:
            file_to_save = make_path_to_download(url, tag[TAG_LINKS[tag.name]])

        filepath_to_save = Path\
            .joinpath(Path(directory),
                      Path(make_modified_path(url,
                                              tag[TAG_LINKS[tag.name]])))

        data = download_tag(file_to_save, bar)
        save_data(data.content, filepath_to_save)
    bar.finish()


def parse_resources(url: str,
                    soup: bs4.BeautifulSoup) -> list:
    tags = soup.find_all(['img', 'link', 'script'])

    resources = []
    for tag in tags:
        if tag.name == 'script' and tag.get(TAG_LINKS[tag.name]) is None:
            continue
        if is_external_link(url, tag, TAG_LINKS[tag.name]):
            continue

        resources.append(tag)

    return resources


def make_directory(url: str,
                   directory: str) -> None:
    files_folder_name = format_host_name(url) + FILES_FOLDER_SUFFIX
    files_path = Path().joinpath(directory, files_folder_name)

    Path.mkdir(files_path, exist_ok=True)


def modify_html(url: str,
                directory: str,
                tags: list) -> str:
    for tag in tags:
        modified_path = make_modified_path(url, tag[TAG_LINKS[tag.name]])
        tag[TAG_LINKS[tag.name]] = modified_path

    html_path = Path().joinpath(directory,
                                format_host_name(url) + HTML_SUFFIX)
    return str(html_path)
