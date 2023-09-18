import logging
from time import sleep

logger = logging.getLogger("querystar")


def time(interval: float = 1.5):
    """
    :param int seconds: trigger wait for `seconds` amount of time before returning
    """

    logger.info('Subscribed TRIGGER - time')
    logger.info('Listening TRIGGER - time')
    sleep(interval)
    logger.info('Recieved TRIGGER - time')
    return {'time_elapsed': interval}
