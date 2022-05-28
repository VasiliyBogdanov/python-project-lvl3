import argparse
from bs4 import BeautifulSoup
import os
from page_loader.logger import page_loader_logger
from page_loader.paths import (is_external_link,
                               make_modified_path,
                               make_path_to_resource,
                               TAG_LINKS,
                               )
import requests
from typing import Tuple

HTML_PARSER = 'html.parser'
logger = page_loader_logger


def parse_cli_arguments() -> Tuple[str, str]:
    parser = argparse.ArgumentParser(
        description="A little parse_cli_arguments utility that lets you download static web pages." # noqa E501
    )
    parser.add_argument("url")
    parser.add_argument("-o", "--output",
                        help="Set output path, "
                             "default is current working directory",
                        default=os.getcwd())

    args = parser.parse_args()
    url, output_path = args.url, args.output

    return url, output_path


def parse_resources(content: requests.Response,
                    directory: str)\
        -> Tuple[str, list[Tuple[str, os.PathLike]]]:
    """Parses downloaded webpage's tags, saves links
     to files (that are local to webpage), makes paths to local
     (to be downloaded) files
    and modifies paths inside downloaded .html
     to point to downloaded resources.

    :param content: webpage content.
    :param directory: directory to save content.
    :return:
        'Prettified' html, List of tuples:
            [0] link from tag,
            [1] path to save resource.
    """
    soup = BeautifulSoup(content.text, HTML_PARSER)
    tags = soup.find_all(TAG_LINKS)

    download_links = []
    for tag in tags:
        if tag.get(TAG_LINKS[tag.name]) is None or\
                is_external_link(content.url, tag[TAG_LINKS[tag.name]]):
            continue
        filepath_to_save = make_path_to_resource(content,
                                                 directory,
                                                 tag)
        download_links.append((tag[TAG_LINKS[tag.name]], filepath_to_save))

        modified_path = make_modified_path(content.url,
                                           tag[TAG_LINKS[tag.name]])
        tag[TAG_LINKS[tag.name]] = modified_path

    return soup.prettify(), download_links
