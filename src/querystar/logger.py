import logging
import traceback
from pprint import pprint
from querystar.settings import settings


class LoggerFormatter(logging.Formatter):
    # Add color to the logger
    COLORS = {
        'DEBUG': '\033[96m',  # Cyan
        'INFO': '\033[92m',   # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',   # Red
        'CRITICAL': '\033[95m',  # Magenta
    }

    RESET = '\033[0m'

    def format(self, record: logging.LogRecord):
        log_record = {
            "grey": "\033[90m",
            "color": self.COLORS.get(record.levelname, ''),
            "asctime": self.formatTime(record, "%Y-%m-%d %H:%M:%S"),
            "levelname": record.levelname,
            "message": super().format(record),
            "reset": self.RESET
        }

        return "{grey}[{asctime}] {color}{levelname:<10}{reset} : {message}".format(**log_record)


class RemoteLoggerHandler(logging.Handler):
    def __init__(self, handler):
        super().__init__()

        self._handler = handler

    def emit(self, record: logging.LogRecord):

        properties = {
            'timestamp': record.created,
            'message': record.msg,
            'pathname': record.pathname,
            'funcName': record.funcName,
            'levelname': record.levelname,
            'app_id': settings.app_id,
        }
        if record.exc_info:
            _excp_traceback = traceback.print_exception(*record.exc_info)
            properties['exc_info'] = _excp_traceback

        event = 'local_querystar_log'
        if 'TRIGGER' in record.msg or 'ACTION' in record.msg:
            _parse_msg = record.msg.split(" ")
            event = f'{_parse_msg[0].lower()}.{_parse_msg[1].lower()}.{_parse_msg[3].lower()}'

        if record.levelname in ['ERROR', 'CRITICAL']:
            event = record.levelname.lower()

        self._handler.capture(
            "user_id:org_id",
            event,
            properties
        )


class FileHandler(logging.Handler):
    def __init__(self, filename, mode='a'):
        super().__init__()
        self.filename = filename
        self.mode = mode

    def emit(self, record):
        with open(self.filename, self.mode) as f:
            f.write(self.format(record) + '\n')


def initialize_logger(app_id: str, fl: bool = False):
    # Initialize and configure the logger
    logger = logging.getLogger("querystar")
    logger.setLevel(logging.INFO)
    # logger.setLevel(logging.DEBUG)

    # Create a console handler with colored output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(LoggerFormatter())
    logger.addHandler(console_handler)

    if fl:
        # Add file logger handler
        file_log_format = '[%(asctime)s] %(levelname)s : %(message)s'
        file_handler = logging.FileHandler(f'{app_id}.log', mode='a')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            file_log_format, datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # # Remote logger handler
        # try:
        #     from querystar.remote_logger import posthog
        #     _remote_logger = RemoteLoggerHandler(handler=posthog)
        #     logger.addHandler(_remote_logger)
        # except Exception as e:
        #     logger.warning(f"No remote logging handler found.")
