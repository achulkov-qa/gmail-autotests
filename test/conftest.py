import logging

from common.journal import logger_name


def l_error(msg):
    logging.error(msg)
    return msg

def get_log():
    return open(logger_name).read()