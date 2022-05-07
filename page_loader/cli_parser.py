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
    parser.add_argument("--log",
                        help="Set to True to enable create log file, "
                             "default is False",
                        default=False)

    args = parser.parse_args()
    url, output_path, log = args.url, args.output, args.log

    print(download(url=url,
                   directory=output_path,
                   log=log))
