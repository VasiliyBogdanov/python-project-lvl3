import argparse
import os
from page_loader import download
from page_loader.logger import page_loader_logger
from requests import ConnectionError
import sys

logger = page_loader_logger


def cli() -> None:
    parser = argparse.ArgumentParser(
        description="A little cli utility that lets you download static web pages." # noqa E501
    )
    parser.add_argument("url")
    parser.add_argument("-o", "--output",
                        help="Set output path, "
                             "default is current working directory",
                        default=os.getcwd())

    args = parser.parse_args()
    url, output_path = args.url, args.output

    try:
        result = download(url=url, directory=output_path)
    except (PermissionError, OSError, ConnectionError):
        sys.exit(1)
    else:
        print(f'Page was successfully downloaded to {result}')
