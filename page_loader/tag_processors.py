import page_loader.K as K
from page_loader.formatters import format_modified_path
from page_loader.formatters import format_filepath_to_save
import os
from page_loader.error_handler import try_to_download
from urllib.parse import urljoin
from urllib.parse import urlparse


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
    if data:
        with open(path, mode=mode) as f:
            f.write(data)
    else:
        return


def preprocess_tags(url, tags, tag_link_attr):
    """Filter out tags with links to external resources."""
    output = []
    for tag in tags:
        if not is_external_link(url, tag, tag_link_attr):
            output.append(tag)
    return output


def process_tag(tag_link_attr, tag, session, url, files_path, logger, bar):
    parsed_tag = urlparse(tag[tag_link_attr])

    if is_absolute_path(url, tag, tag_link_attr):
        file_to_save = tag[tag_link_attr]
    else:
        file_to_save = os.path.join(url, tag[tag_link_attr][1:])\
            if tag.name == K.TAG_NAMES.img\
            else urljoin(url, parsed_tag.path)

    filepath_to_save = format_filepath_to_save(url, parsed_tag, files_path)

    data = try_to_download(session, file_to_save, logger, bar)
    save_data(data.content if tag.name == K.TAG_NAMES.img else data.text,
              filepath_to_save,
              'wb' if tag.name == K.TAG_NAMES.img else 'w')

    img_path_modified = format_modified_path(url,
                                             parsed_tag.path
                                             if tag.name == K.TAG_NAMES.img
                                             else tag[tag_link_attr],
                                             K.FILES_FOLDER_SUFFIX)
    tag[tag_link_attr] = img_path_modified


def process_tags(data, session, url, files_path, logger, bar):
    resources = session, url, files_path, logger, bar
    for tag in data.img:
        process_tag(K.TAG_LINKS.img, tag, *resources)
    for tag in data.link:
        process_tag(K.TAG_LINKS.link, tag, *resources)
    for tag in data.script:
        process_tag(K.TAG_LINKS.script, tag, *resources)
