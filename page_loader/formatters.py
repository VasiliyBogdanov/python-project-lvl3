import os
import string
from urllib.parse import urlparse


def format_filename(url: str, ext: str) -> str:
    parsed_url = urlparse(url, scheme='http')

    url_path = os.path.splitext(parsed_url.path)[0]
    url_path = url_path[:-1] if url_path.endswith('/') else url_path

    path_str = "".join((parsed_url.netloc, url_path))
    filename = ''.join(i if i not in string.punctuation
                       else '-'
                       for i in path_str) + ext
    return filename
