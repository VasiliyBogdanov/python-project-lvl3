import argparse
import os
from page_loader.logger import page_loader_logger
from typing import Tuple


logger = page_loader_logger


def parse_arguments() -> Tuple[str, str]:
    parser = argparse.ArgumentParser(
        description="A little parse_arguments utility that lets you download static web pages." # noqa E501
    )
    parser.add_argument("url")
    parser.add_argument("-o", "--output",
                        help="Set output path, "
                             "default is current working directory",
                        default=os.getcwd())

    args = parser.parse_args()
    url, output_path = args.url, args.output

    return url, output_path
