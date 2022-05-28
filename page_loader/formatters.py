import os
import string
from urllib.parse import urlparse

SCHEME = 'http'
FILENAME_DELIMITER = '-'


def format_filename(url: str) -> str:
    parsed_url = urlparse(url).netloc + urlparse(url).path
    path, ext = os.path.splitext(parsed_url)
    path = path.rstrip('/')
    filename = format_url(path) + ext
    return filename


def format_host_name(home_url: str) -> str:
    home_url = home_url.rstrip('/')
    parsed_home_url = urlparse(home_url)
    formatted_host = format_url(parsed_home_url.netloc + parsed_home_url.path)
    return formatted_host


def format_url(elem: str) -> str:
    formatted_elem = ''.join(i if i not in string.punctuation
                             else FILENAME_DELIMITER
                             for i in elem)
    return formatted_elem
