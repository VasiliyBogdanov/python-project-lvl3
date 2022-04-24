from bs4 import BeautifulSoup
import os
import pathlib
import requests
import string
from urllib.parse import urlparse


def download(url: str, directory: str = None) -> str:
    if directory is None:
        directory = os.getcwd()
    if not pathlib.Path(directory).exists():
        raise OSError("Directory does not exist")

    content = requests.get(url).text

    html_path = os.path.join(directory, format_filename(url, ext='.html'))
    files_suffix = format_filename(url, ext='_files')
    files_path = os.path.join(directory, files_suffix)

    # Create directory for downloaded files
    if not pathlib.Path(files_path).exists():
        os.mkdir(files_path)

    # Parse html for img tags
    soup = BeautifulSoup(content, 'html.parser')
    images = soup.find_all('img', recursive=True)

    # Download img, if .png or .jpg
    session = requests.Session()
    for i in images:
        image_path, image_ext = os.path.splitext(i['src'])
        if image_ext in ('.png', '.jpg'):
            image_name = format_filename(image_path[1:], image_ext)
            formatted_img_path = i['src'][1:] \
                if str(i['src']).startswith('/') \
                else i['src']
            img_download_path = os.path.join(url, formatted_img_path)
            img_save_path = os.path.join(files_path, image_name)

            # Download image
            img_to_save = session.get(img_download_path, stream=True)

            # Save downloaded image
            save_img(img_to_save, img_save_path)

            # Modify img links inside downloaded html
            img_path_modified = os.path.join(files_suffix, image_name)
            i['src'] = img_path_modified

    # Save modified html
    with open(html_path, mode='w') as output_html:
        output_html.write(soup.prettify())

    return html_path


def save_img(img, path):
    with open(path, mode='wb') as f:
        f.write(img.content)


def format_filename(url: str, ext: str) -> str:
    parsed_url = urlparse(url, scheme='http')

    url_path = os.path.splitext(parsed_url.path)[0]
    url_path = url_path[:-1] if url_path.endswith('/') else url_path

    path_str = "".join((parsed_url.netloc, url_path))
    filename = ''.join(i if i not in string.punctuation
                       else '-'
                       for i in path_str) + ext
    return filename
