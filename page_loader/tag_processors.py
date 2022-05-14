import page_loader.K as K
from page_loader.formatters import format_filename
from pathlib import Path
import os
from page_loader.error_handler import try_to_download_tag
from urllib.parse import urljoin
from urllib.parse import urlparse


def make_modified_path(home_url, tag_url):
    host = urlparse(home_url).netloc
    left_side = format_filename(home_url) + K.FILES_FOLDER_SUFFIX
    path, ext = os.path.splitext(tag_url)
    path = path[1:] if path.startswith('/') else path

    if urlparse(path).scheme:
        right_side = format_filename(path) + ext
    elif not urlparse(path).scheme and not ext:
        right_side = format_filename(home_url) + K.HTML_SUFFIX
    else:
        right_side = format_filename(os.path.join(format_filename(host),
                                                  path)) + ext
    return os.path.join(left_side, right_side)


def make_path_to_download(home_url: str, tag_url: str):
    home_url = home_url if home_url.endswith('/') else home_url + '/'
    return urljoin(home_url, tag_url)


def is_absolute_path(url, tag, tag_link_attr):
    parsed_url = urlparse(url)
    parsed_tag = urlparse(tag[tag_link_attr])
    if parsed_tag.scheme and parsed_tag.netloc == parsed_url.netloc:
        return True
    return False


def is_external_link(home_url, tag, tag_link_attr):
    """If False, link is considered internal."""
    parsed_tag = urlparse(tag[tag_link_attr])
    if is_absolute_path(home_url, tag, tag_link_attr) or \
            not parsed_tag.scheme:
        return False
    return True


def save_data(data, path, mode):
    """Wrapper for saving data."""
    with open(path, mode=mode) as f:
        f.write(data)


def preprocess_tags(url, tags, tag_link_attr):
    """Filter out tags with links to external resources."""
    output = []
    for tag in tags:
        if not is_external_link(url, tag, tag_link_attr):
            output.append(tag)
    return output


def process_tag(tag_link_attr, tag, session, url, directory, logger, bar):
    if is_absolute_path(url, tag, tag_link_attr):
        file_to_save = tag[tag_link_attr]
    else:
        file_to_save = make_path_to_download(url, tag[tag_link_attr])

    filepath_to_save = Path\
        .joinpath(Path(directory),
                  Path(make_modified_path(url,
                                          tag[tag_link_attr])))

    data = try_to_download_tag(session, file_to_save, logger, bar)
    save_data(data.content, filepath_to_save, 'wb')
    #               'wb' if tag.name == K.TAG_NAMES.img else 'w'
    # if tag.name == K.TAG_NAMES.img else data.text
    modified_path = make_modified_path(url, tag[tag_link_attr])
    tag[tag_link_attr] = modified_path


def process_tags(data, session, url, directory, logger, bar):
    resources = session, url, directory, logger, bar
    for tag in data.img:
        process_tag(K.TAG_LINKS.img, tag, *resources)
    for tag in data.link:
        process_tag(K.TAG_LINKS.link, tag, *resources)
    for tag in data.script:
        process_tag(K.TAG_LINKS.script, tag, *resources)
