import logging
from logging.handlers import RotatingFileHandler
from logging import StreamHandler


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
        console_handler = StreamHandler()
        console_handler.setFormatter(log_format)
        self.logger.addHandler(console_handler)

    def log_request_success(self, vps):
        self.logger.info(f"The request was successfully processed on the VPS: {vps}")

    def log_request_error(self, vps, error):
        self.logger.error(f"An error occurred on the VPS: {vps}")
        self.logger.error(f"Error: {error}")
