#!/usr/bin/env python3
from page_loader.cli import parse_arguments
from page_loader.page_loader import download
from requests import (HTTPError,
                      ConnectionError,
                      Timeout)
import sys


def main():
    url, output_path = parse_arguments()

    try:
        result = download(url=url, directory=output_path)
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
