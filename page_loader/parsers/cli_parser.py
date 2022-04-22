import argparse
from page_loader import download
import os


def cli_arg_parser():
    parser = argparse.ArgumentParser(
        description="A little cli utility that lets you download web pages."
    )
    parser.add_argument("url")
    parser.add_argument("--output",
                        help="Set output path",
                        default=os.getcwd())

    args = parser.parse_args()
    url, output_path = args.url, args.output

    print(download(url=url,
                   directory=output_path))
