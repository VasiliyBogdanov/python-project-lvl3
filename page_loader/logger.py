import logging


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    return logger


def get_standard_file_handler(log_dir, delay=True, mode='a'):
    file_handler = logging.FileHandler(log_dir, delay=delay, mode=mode)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(get_standard_log_formatter())
    return file_handler


def get_standard_log_formatter():
    return logging.Formatter('%(asctime)s:%(name)s:%(message)s')


page_loader_logger = get_logger('page-loader')
page_loader_logger.addHandler(get_standard_file_handler('info.log', mode='w'))
