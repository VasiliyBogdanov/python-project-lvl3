import logging

LOG_FORMAT = '%(asctime)s:%(name)s:%(message)s'


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    return logger


def get_standard_file_handler(log_dir: str,
                              delay: bool = True,
                              mode: str = 'a') -> logging.FileHandler:
    file_handler = logging.FileHandler(log_dir, delay=delay, mode=mode)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(get_file_log_formatter(LOG_FORMAT))
    return file_handler


def get_standard_stream_handler() -> logging.StreamHandler:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(get_file_log_formatter(' ' + LOG_FORMAT))
    return stream_handler


def get_file_log_formatter(log_format: str) -> logging.Formatter:
    return logging.Formatter(log_format)


def get_main_logger() -> logging.Logger:
    main_logger = get_logger('page-loader')
    main_logger.addHandler(get_standard_file_handler('info.log', mode='w'))
    main_logger.addHandler(get_standard_stream_handler())
    return main_logger


page_loader_logger = get_main_logger()
