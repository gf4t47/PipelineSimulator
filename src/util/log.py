import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.disable(logging.DEBUG)


def log(*argv):
    logging.debug(*argv)


def log_err(*argv):
    logging.error(*argv)
    sys.exit(-1)
