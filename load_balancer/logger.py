import logging
from logging.handlers import RotatingFileHandler
from logging import StreamHandler
import sys


class Logger:
    def __init__(self, log_file='log.txt', log_level=logging.INFO):
        self.logger = logging.getLogger('load_balancer')
        self.logger.setLevel(log_level)

        # Log entry format
        log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Handler for writing to a file with rotation
        file_handler = RotatingFileHandler(log_file, maxBytes=1024, backupCount=5)
        file_handler.setFormatter(log_format)
        self.logger.addHandler(file_handler)

        # Handler for writing to the console
        console_handler = StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        self.logger.addHandler(console_handler)

        # Separate file handlers for different log levels
        self.error_file_handler = RotatingFileHandler('error.log', maxBytes=1024, backupCount=5)
        self.error_file_handler.setLevel(logging.ERROR)
        self.error_file_handler.setFormatter(log_format)
        self.logger.addHandler(self.error_file_handler)

    def set_log_level(self, log_level):
        self.logger.setLevel(log_level)

    def log_request_success(self, vps):
        self.logger.info(f"The request was successfully processed on the VPS: {vps}")

    def log_request_error(self, vps, error):
        self.logger.error(f"An error occurred on the VPS: {vps}")
        self.logger.error(f"Error: {error}")

    def log_debug(self, message):
        self.logger.debug(message)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)
        self.error_file_handler.emit(logging.makeLogRecord({
            'levelname': 'ERROR',
            'message': message
        }))

    def log_critical(self, message):
        self.logger.critical(message)
        self.error_file_handler.emit(logging.makeLogRecord({
            'levelname': 'CRITICAL',
            'message': message
        }))
