#!/usr/bin/env python3
import sys

from requests import (HTTPError,
                      ConnectionError,
                      Timeout)

from page_loader.page_loader import download
from page_loader.parsers import parse_cli_arguments


def main():
    url, directory = parse_cli_arguments()

    try:
        result = download(url=url, directory=directory)
    except (ConnectionError,
            HTTPError,
            OSError,
            PermissionError,
            Timeout,
            ):
        sys.exit(1)
    else:
        print(f'Page was successfully downloaded to {result}')


if __name__ == '__main__':
    main()
