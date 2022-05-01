from page_loader.formatters import format_filename
import os
from urllib.parse import urljoin
from urllib.parse import urlparse


def _download_images(*, session, images, url, files_path):
    files_folder_name = files_path.split('/')[-1]
    for i in images:
        image_path, image_ext = os.path.splitext(i['src'])
        if image_ext in ('.png', '.jpg'):
            image_name = format_filename(image_path[1:], image_ext)
            img_download_path = os.path.join(url, i['src'][1:])
            img_save_path = os.path.join(files_path, image_name)

            img_to_save = session.get(img_download_path, stream=True)

            with open(img_save_path, mode='wb') as f:
                f.write(img_to_save.content)

            img_path_modified = os.path.join(files_folder_name, image_name)

            i['src'] = img_path_modified


def _download_links(*, session, links, url, files_path):
    files_folder_name = files_path.split('/')[-1]
    parsed_url = urlparse(url)
    home_url_host = parsed_url.netloc

    for i in links:
        parsed_link = urlparse(i['href'])

        # If i is absolute link and domain == our site's domain
        if parsed_link.scheme and parsed_link.netloc == home_url_host:
            file_to_save = session.get(i['href'])

            path, ext = os.path.splitext(parsed_link.path)
            filename_to_join = format_filename(path[1:], ext)
            filepath_to_save = os.path.join(files_path, filename_to_join)

            with open(filepath_to_save, mode='w') as f:
                f.write(file_to_save.text)

            modified_path = os.path.join(files_folder_name, filename_to_join)

            i['href'] = modified_path

        # If i is a relative link
        elif not parsed_link.scheme:
            path, ext = os.path.splitext(parsed_link.path)
            ext = ext if ext else '.html'
            filename_to_join = format_filename(path[1:], ext)
            filepath_to_save = os.path.join(files_path, filename_to_join)
            file_to_save = urljoin(url, parsed_link.path)

            downloaded_link = session.get(file_to_save, stream=True)

            with open(filepath_to_save, mode='w') as f:
                f.write(downloaded_link.text)

            modified_path = os.path.join(files_folder_name, filename_to_join)

            i['href'] = modified_path


def _download_scripts(*, session, scripts, url, files_path):
    files_folder_name = files_path.split('/')[-1]
    parsed_url = urlparse(url)
    home_url_host = parsed_url.netloc

    for i in scripts:
        # If i is not inline script
        if i.get('src'):
            parsed_script = urlparse(i['src'])

            # If i is an absolute link and domain == our site's domain
            if parsed_script.scheme and parsed_script.netloc == home_url_host:
                file_to_save = session.get(i['src'])

                path, ext = os.path.splitext(parsed_script.path)
                filename_to_join = format_filename(path[1:], ext)
                filepath_to_save = os.path.join(files_path, filename_to_join)

                with open(filepath_to_save, mode='w') as f:
                    f.write(file_to_save.text)

                modified_path = os.path.join(files_folder_name,
                                             filename_to_join)

                i['src'] = modified_path

            # If i is a relative link
            elif not parsed_script.scheme:
                path, ext = os.path.splitext(parsed_script.path)
                filename_to_join = format_filename(path[1:], ext)
                filepath_to_save = os.path.join(files_path, filename_to_join)
                file_to_save = urljoin(url, parsed_script.path)

                downloaded_script = session.get(file_to_save, stream=True)

                with open(filepath_to_save, mode='w') as f:
                    f.write(downloaded_script.text)

                modified_path = os.path.join(files_folder_name,
                                             filename_to_join)

                i['src'] = modified_path


def download_resources(session, resources, url, files_path):
    _download_images(session=session,
                     images=resources.images,
                     url=url,
                     files_path=files_path)

    _download_links(session=session,
                    links=resources.links,
                    url=url,
                    files_path=files_path)

    _download_scripts(session=session,
                      scripts=resources.scripts,
                      url=url,
                      files_path=files_path)
