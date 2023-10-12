import logging


def log():
    logger = logging.getLogger(__name__)

    formatter = logging.Formatter(
        '[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
    )

    stream_handler = logging.StreamHandler()
