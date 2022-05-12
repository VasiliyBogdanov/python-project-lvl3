import page_loader.K as K
import os
import string
from urllib.parse import urlparse

SCHEME = 'http'
FILENAME_DELIMITER = '-'


def format_filename(url: str, ext: str = "") -> str:
    parsed_url = urlparse(url, scheme=SCHEME)

    url_path = os.path.splitext(parsed_url.path)[0]
    url_path = url_path[:-1] if url_path.endswith('/') else url_path

    path_str = "".join((parsed_url.netloc, url_path))

    filename = ''.join(i if i not in string.punctuation
                       else FILENAME_DELIMITER
                       for i in path_str) + ext
    return filename


def format_url(elem: str):
    formatted_elem = ''.join(i if i not in string.punctuation
                             else FILENAME_DELIMITER
                             for i in elem)
    return formatted_elem


def format_modified_path(home_url: str, url: str, files_suffix: str):
    parsed_home_url = urlparse(home_url)
    parsed_url = urlparse(url)
    formatted_host = format_url(parsed_home_url.netloc)
    left_part = format_url(parsed_home_url.netloc
                           + parsed_home_url.path) + files_suffix
    path, ext = os.path.splitext(parsed_url.path)
    ext = ext = ext if ext else K.HTML_SUFFIX
    formatted_path = format_url(path)
    right_part = formatted_host + formatted_path + ext

    formatted_modified_path = os.path.join(left_part, right_part)
    return formatted_modified_path


def format_filepath_to_save(url, link, files_path):
    path, ext = os.path.splitext(link.path)
    ext = ext if ext else K.HTML_SUFFIX
    filename_to_join = format_filename(url, '-')\
        + format_filename(path[1:], ext)
    filepath_to_save = os.path.join(files_path, filename_to_join)
    return filepath_to_save


def format_host_name(home_url: str):
    parsed_home_url = urlparse(home_url)
    formatted_host = format_url(parsed_home_url.netloc)
    return formatted_host
