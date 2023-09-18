import logging


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
