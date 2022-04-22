import requests
import os
import pathlib
import string
from urllib.parse import urlparse


def download(url: str, directory: str = None) -> str:
    """
    Downloads web page
    :param url: Full URL
    :param directory: Path to save downloaded file, default is cwd.
    Must be existing directory or OSError will be raised.
    :return: Full path to saved file
    """
    if directory is None:
        directory = os.getcwd()
    if not pathlib.Path(directory).exists():
        raise OSError("Directory does not exist")

    content = requests.get(url).text
    write_directory = os.path.join(directory, format_filename(url))

    with open(write_directory, mode='w') as f:
        f.write(content)

    return write_directory


def format_filename(url: str) -> str:
    """
    Makes filename from full URL.
    Example:
    url = https://www.google.com
    Function returns: www-google-com.html
    :param url: Full URL
    :return: Formatted filename
    """
    parsed_url = urlparse(url, scheme='http')

    url_path = os.path.splitext(parsed_url.path)[0]
    url_path = url_path[:-1] if url_path.endswith('/') else url_path

    path_str = "".join((parsed_url.netloc, url_path))
    formatted_url = ''.join(i if i not in string.punctuation
                            else '-'
                            for i in path_str) + '.html'
    return formatted_url
