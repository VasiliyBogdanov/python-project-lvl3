import page_loader.K as K
import os
import string
from urllib.parse import urlparse

SCHEME = 'http'
FILENAME_DELIMITER = '-'


def format_filename(url: str):
    parsed_url = urlparse(url).netloc + urlparse(url).path
    path, ext = os.path.splitext(parsed_url)
    path = path.rstrip('/')
    filename = ''.join(i if i not in string.punctuation
                       else FILENAME_DELIMITER
                       for i in path) + ext
    return filename


def format_url(elem: str):
    formatted_elem = ''.join(i if i not in string.punctuation
                             else FILENAME_DELIMITER
                             for i in elem)
    return formatted_elem


def format_filepath_to_save(url, link, files_path):
    path, ext = os.path.splitext(link.path)
    ext = ext if ext else K.HTML_SUFFIX
    filename_to_join = format_filename(url) + '-'\
        + format_filename(path[1:]) + ext
    filepath_to_save = os.path.join(files_path, filename_to_join)
    return filepath_to_save


def format_host_name(home_url: str):
    parsed_home_url = urlparse(home_url)
    formatted_host = format_url(parsed_home_url.netloc)
    return formatted_host
