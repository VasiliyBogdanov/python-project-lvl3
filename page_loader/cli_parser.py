import argparse
import os
from page_loader.logger import page_loader_logger
from page_loader import download
from requests import ConnectionError
import sys

logger = page_loader_logger


def cli_arg_parser():
    parser = argparse.ArgumentParser(
        description="A little cli utility that lets you download static web pages." # noqa E501
    )
    parser.add_argument("url")
    parser.add_argument("--output",
                        help="Set output path, "
                             "default is current directory",
                        default=os.getcwd())
    parser.add_argument("--log",
                        help="Set to True to enable create log file, "
                             "default is False",
                        default=False)

    args = parser.parse_args()
    url, output_path, log = args.url, args.output, args.log

    try:
        print(download(url=url,
                       directory=output_path,
                       log=log))
    except (PermissionError, OSError, ConnectionError):
        sys.exit(1)
