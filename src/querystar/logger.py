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
    def emit(self, record: logging.LogRecord):
        from querystar.remote_logger import posthog

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

        posthog.capture(
            "user_id:org_id",
            event,
            properties
        )


def initialize_logger(rl: bool = False):
    # Initialize and configure the logger
    logger = logging.getLogger("querystar")
    logger.setLevel(logging.INFO)
    # logger.setLevel(logging.DEBUG)

    # Create a console handler with colored output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(LoggerFormatter())
    logger.addHandler(console_handler)

    if rl:
        try:
            _remote_logger = RemoteLoggerHandler()
            logger.addHandler(_remote_logger)
        except Exception as e:
            logger.debug(f"No remote logging handler found.")
