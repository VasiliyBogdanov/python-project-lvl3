from page_loader.logger import page_loader_logger
from page_loader.formatters import format_filename
import os
from requests.exceptions import HTTPError
import sys
from urllib.parse import urljoin
from urllib.parse import urlparse

logger = page_loader_logger


def process_img_tag(img, session, url, files_path, files_folder_name):
    parsed_image = urlparse(img['src'])

    path, ext = os.path.splitext(parsed_image.path)
    filename_to_join = format_filename(path[1:], ext)
    filepath_to_save = os.path.join(files_path, filename_to_join)

    if ext in ('.png', '.jpg'):
        img_download_path = os.path.join(url, img['src'][1:])
        data = _try_to_download(session, img_download_path)
        if data:
            with open(filepath_to_save, mode='wb') as f:
                f.write(data.content)
        else:
            return

        img_path_modified = os.path.join(files_folder_name, filename_to_join)
        img['src'] = img_path_modified


def process_link_tag(link, session, url, files_path, files_folder_name):
    parsed_url = urlparse(url)
    home_url_host = parsed_url.netloc

    parsed_link = urlparse(link['href'])

    path, ext = os.path.splitext(parsed_link.path)
    filename_to_join = format_filename(path[1:], ext)
    filepath_to_save = os.path.join(files_path, filename_to_join)

    if parsed_link.scheme and parsed_link.netloc == home_url_host:
        data = _try_to_download(session, link['href'])
        if data:
            with open(filepath_to_save, mode='w') as f:
                f.write(data.text)
        else:
            return

        modified_path = os.path.join(files_folder_name, filename_to_join)
        link['href'] = modified_path

    elif not parsed_link.scheme:
        file_to_save = urljoin(url, parsed_link.path)

        ext = ext if ext else '.html'
        filename_to_join = format_filename(path[1:], ext)
        filepath_to_save = os.path.join(files_path, filename_to_join)

        data = _try_to_download(session, file_to_save)
        if data:
            with open(filepath_to_save, mode='w') as f:
                f.write(data.text)
        else:
            return

        modified_path = os.path.join(files_folder_name, filename_to_join)
        link['href'] = modified_path


def process_script_tag(script, session, url, files_path, files_folder_name):
    if script.get('src'):
        parsed_url = urlparse(url)
        home_url_host = parsed_url.netloc
        parsed_script = urlparse(script['src'])

        path, ext = os.path.splitext(parsed_script.path)
        filename_to_join = format_filename(path[1:], ext)
        filepath_to_save = os.path.join(files_path, filename_to_join)

        if parsed_script.scheme and parsed_script.netloc == home_url_host:
            data = _try_to_download(session, script['src'])

            if data:
                with open(filepath_to_save, mode='w') as f:
                    f.write(data.text)
            else:
                return

            modified_path = os.path.join(files_folder_name, filename_to_join)

            script['src'] = modified_path

        elif not parsed_script.scheme:
            file_to_save = urljoin(url, parsed_script.path)
            data = _try_to_download(session, file_to_save)

            if data:
                with open(filepath_to_save, mode='w') as f:
                    f.write(data.text)
            else:
                return

            modified_path = os.path.join(files_folder_name, filename_to_join)

            script['src'] = modified_path


def process_tags(data, session, url, files_path, files_folder_name):
    resources = session, url, files_path, files_folder_name
    for tag in data:
        if tag.name == 'img':
            process_img_tag(tag, *resources)
        elif tag.name == 'link':
            process_link_tag(tag, *resources)
        elif tag.name == 'script':
            process_script_tag(tag, *resources)


def _try_to_download(session, download_path):
    try:
        data_to_save = session.get(download_path, stream=True)
        data_to_save.raise_for_status()
    except HTTPError:
        logger.error(sys.exc_info()[1])
    else:
        logger.info(f'{data_to_save.status_code} '
                    f'{data_to_save.reason} '
                    f'{download_path}')
        return data_to_save
