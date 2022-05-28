import logging

LOG_FORMAT = '%(asctime)s:%(name)s:%(message)s'


def get_file_log_formatter(log_format: str) -> logging.Formatter:
    return logging.Formatter(log_format)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    return logger


def get_main_logger() -> logging.Logger:
    main_logger = get_logger('page-loader')
    main_logger.addHandler(get_standard_stream_handler())
    return main_logger


def get_standard_stream_handler() -> logging.StreamHandler:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(get_file_log_formatter(' ' + LOG_FORMAT))
    return stream_handler


page_loader_logger = get_main_logger()
