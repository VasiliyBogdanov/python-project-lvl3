from bs4 import BeautifulSoup
from collections import namedtuple
import os
import page_loader.K as K
from page_loader.error_handler import try_to_download_page
from page_loader.logger import page_loader_logger
from page_loader.error_handler import make_error
from page_loader.formatters import format_filename
from page_loader.tag_processors import preprocess_tags
from page_loader.tag_processors import process_tags
import pathlib
from progress.bar import Bar
import re
import requests


_resource_tags = namedtuple('Resources', 'img link script')

logger = page_loader_logger


def download(url: str, directory: str = None, *, log: bool = False,
             logger=logger) -> str:
    if not pathlib.Path(directory).exists():
        make_error(OSError,
                   f'Directory \'{directory}\' does not exist',
                   logger)

    if directory is None:
        directory = os.getcwd()
    elif not os.access(directory, mode=os.W_OK):
        make_error(PermissionError,
                   f'You don\'t have rights to write to {directory}',
                   logger)

    if not log:
        logger.disabled = True

    session = requests.Session()
    url = url.rstrip('/')

    content = try_to_download_page(session, url)

    html_path = os.path.join(directory,
                             format_filename(url)) + K.HTML_SUFFIX
    files_folder_name = format_filename(url) + K.FILES_FOLDER_SUFFIX
    files_path = os.path.join(directory,
                              files_folder_name)

    pathlib.Path.mkdir(pathlib.Path(files_path), exist_ok=True)

    soup = BeautifulSoup(content, 'html.parser')
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

    resource_tags = _resource_tags(img_tags, link_tags, script_tags)
    resource_len = len([*resource_tags.img,
                        *resource_tags.link,
                        *resource_tags.script])

    bar = Bar(max=resource_len)
    process_tags(resource_tags, session, url, files_path,
                 logger, bar)

    with open(html_path, mode='w') as output_html:
        output_html.write(soup.prettify())

    bar.finish()

    return html_path
