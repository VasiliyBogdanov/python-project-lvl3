from page_loader.formatters import format_host_name
from page_loader.paths import HTML_SUFFIX
from pathlib import Path
import os


def save_page(html: str,
              url: str,
              directory: str) -> str:
    """Saves downloaded webpage with modified links,
     so they point to downloaded resources.

    :param html: 'Prettified' html file
    :param url: webpage url to download
    :param directory: directory to save webpage .html file with its resources.
            For resource files new folder will be created with
             '_files' suffix inside this directory.
    :return: Path to saved html file.
    """
    html_path = Path().joinpath(directory,
                                format_host_name(url) + HTML_SUFFIX)

    with open(html_path, mode='w') as output_html:
        output_html.write(html)

    return str(html_path)


def save_data(data: bytes,
              path: os.PathLike) -> None:
    """Wrapper for saving data."""
    with open(path, mode='wb') as f:
        f.write(data)
