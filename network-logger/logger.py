import logging
from logging.handlers import RotatingFileHandler
import json

class Logger:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            cfg = json.load(f)
        self.logger = logging.getLogger("SecurityLogger")
        self.logger.setLevel(logging.DEBUG)
        handler = RotatingFileHandler(cfg["log_file"], maxBytes=cfg["max_log_size"], backupCount=cfg["backup_count"])
        formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def info(self, msg: str):
        self.logger.info(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)
