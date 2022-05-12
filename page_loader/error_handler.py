from page_loader.logger import page_loader_logger
from requests import HTTPError, ConnectionError
import sys

logger = page_loader_logger


def make_error(err_type, msg, logger):
    try:
        raise err_type(msg)
    except err_type:
        logger.error(sys.exc_info()[1])
        raise


def try_to_download(session, download_path, logger, bar):
    try:
        data_to_save = session.get(download_path, stream=True)
        data_to_save.raise_for_status()
    except (HTTPError, ConnectionError):
        bar.next()
        logger.error(sys.exc_info()[1])
        raise
    else:
        bar.next()
        logger.info(f'{data_to_save.status_code} '
                    f'{data_to_save.reason} '
                    f'{download_path}')

        return data_to_save
