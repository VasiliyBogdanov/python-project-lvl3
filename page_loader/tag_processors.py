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


def process_img_tag(img, session, url, files_path, logger, bar):
    parsed_image = urlparse(img[K.TAG_LINKS.img])

    if is_absolute_path(url, img, K.TAG_LINKS.img):
        file_to_save = img[K.TAG_LINKS.img]
    else:
        file_to_save = os.path.join(url, img[K.TAG_LINKS.img][1:])

    filepath_to_save = format_filepath_to_save(parsed_image, files_path)

    data = try_to_download(session, file_to_save, logger, bar)
    save_data(data.content, filepath_to_save, 'wb')

    img_path_modified = format_modified_path(url,
                                             parsed_image.path,
                                             K.FILES_FOLDER_SUFFIX)
    img[K.TAG_LINKS.img] = img_path_modified


def process_link_tag(link, session, url, files_path, logger, bar):
    parsed_link = urlparse(link[K.TAG_LINKS.link])

    filepath_to_save = format_filepath_to_save(parsed_link, files_path)

    if is_absolute_path(url, link, K.TAG_LINKS.link):
        file_to_save = link[K.TAG_LINKS.link]
    else:
        file_to_save = urljoin(url, parsed_link.path)

    data = try_to_download(session, file_to_save, logger, bar)
    save_data(data.text, filepath_to_save, 'w')

    link_path_modified = format_modified_path(url,
                                              link[K.TAG_LINKS.link],
                                              K.FILES_FOLDER_SUFFIX)
    link[K.TAG_LINKS.link] = link_path_modified


def process_script_tag(script, session, url, files_path, logger, bar):
    parsed_script = urlparse(script[K.TAG_LINKS.script])

    filepath_to_save = format_filepath_to_save(parsed_script, files_path)

    if is_absolute_path(url, script, K.TAG_LINKS.script):
        file_to_save = script[K.TAG_LINKS.script]

    else:
        file_to_save = urljoin(url, parsed_script.path)

    data = try_to_download(session, file_to_save, logger, bar)
    save_data(data.text, filepath_to_save, 'w')

    script_path_modified = format_modified_path(url,
                                                script[K.TAG_LINKS.script],
                                                K.FILES_FOLDER_SUFFIX)
    script[K.TAG_LINKS.script] = script_path_modified


def process_tags(data, session, url, files_path, logger, bar):
    resources = session, url, files_path, logger, bar
    for i in data.img:
        process_img_tag(i, *resources)
    for i in data.link:
        process_link_tag(i, *resources)
    for i in data.script:
        process_script_tag(i, *resources)
