import logging
import bs4
import requests
import page_loader.K as K
from page_loader.formatters import format_filename
from page_loader.formatters import format_host_name
from pathlib import Path
import os
from page_loader.error_handler import try_to_download_tag
import progress.bar
import re
from typing import Union
from typing import Tuple
from urllib.parse import urljoin
from urllib.parse import urlparse


def make_modified_path(home_url: str,
                       tag_url: str) -> str:
    host = urlparse(home_url).netloc
    left_side = format_host_name(home_url) + '_files'
    path, ext = os.path.splitext(tag_url)
    path = path[1:] if path.startswith('/') else path
    ext = ext if ext else '.html'

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


def preprocess_tags(url: str,
                    tags: Union[bs4.ResultSet, list],
                    tag_link_attr: str) -> list:
    """Filter out tags with links to external resources."""
    output = []
    for tag in tags:
        if not is_external_link(url, tag, tag_link_attr):
            output.append(tag)
    return output


def process_tag(tag_link_attr: str,
                tag: bs4.Tag,
                session: requests.Session,
                url: str,
                directory: str,
                logger: logging.Logger,
                bar: progress.bar.Bar) -> None:
    if is_absolute_path(url, tag, tag_link_attr):
        file_to_save = tag[tag_link_attr]
    else:
        file_to_save = make_path_to_download(url, tag[tag_link_attr])

    filepath_to_save = Path\
        .joinpath(Path(directory),
                  Path(make_modified_path(url,
                                          tag[tag_link_attr])))

    data = try_to_download_tag(session, file_to_save, logger, bar)
    save_data(data.content, filepath_to_save)

    modified_path = make_modified_path(url, tag[tag_link_attr])
    tag[tag_link_attr] = modified_path


def process_tags(data: K._resource_tags,
                 session: requests.Session,
                 url: str,
                 directory: str,
                 logger: logging.Logger,
                 bar: progress.bar.Bar) -> None:
    resources = session, url, directory, logger, bar
    for tag in data.img:
        process_tag(K.TAG_LINKS.img, tag, *resources)
    for tag in data.link:
        process_tag(K.TAG_LINKS.link, tag, *resources)
    for tag in data.script:
        process_tag(K.TAG_LINKS.script, tag, *resources)


def prepare_resources(soup: bs4.BeautifulSoup,
                      url: str) -> Tuple[K._resource_tags, int]:
    img_tags = preprocess_tags(url,
                               soup.find_all(K.TAG_NAMES.img,
                                             src=re.compile(r'\.jpg|\.png')),
                               K.TAG_LINKS.img)
    link_tags = preprocess_tags(url,
                                soup.find_all(K.TAG_NAMES.link),
                                K.TAG_LINKS.link)
    script_tags = preprocess_tags(url,
                                  [i for i in soup.find_all(K.TAG_NAMES.script)
                                   if i.get(K.TAG_LINKS.script)],
                                  K.TAG_LINKS.script)

    resource_tags = K._resource_tags(img_tags, link_tags, script_tags)
    resource_len = len([*resource_tags.img,
                        *resource_tags.link,
                        *resource_tags.script])
    return resource_tags, resource_len
