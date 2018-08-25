import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.disable(logging.DEBUG)


def log_err(*argv, quited=False):
    logging.error(*argv)
    if quited:
        sys.exit(-1)


def log(*argv):
    logging.debug(*argv)
