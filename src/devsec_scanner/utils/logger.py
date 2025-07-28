
import logging
import sys
import time
import json
from rich.console import Console
from rich.logging import RichHandler
from colorama import Fore, Style

console = Console()

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'level': record.levelname,
            'name': record.name,
            'message': record.getMessage(),
            'time': self.formatTime(record, self.datefmt),
            'funcName': record.funcName,
            'lineno': record.lineno,
        }
        if record.exc_info:
            log_record['exc_info'] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def get_logger(name, verbose=False, json_mode=False, log_file=None, suppress=False):
    logger = logging.getLogger(name)
    logger.propagate = False
    if suppress:
        logger.disabled = True
        return logger
    if json_mode:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
    else:
        handler = RichHandler(console=console, show_time=True, show_level=True, show_path=verbose, markup=True)
        handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))
    if not logger.handlers:
        logger.addHandler(handler)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(name)s: %(message)s'))
            logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    return logger

def log_performance(logger, label, start_time):
    elapsed = time.time() - start_time
    logger.info(f"{Fore.YELLOW}⏱️ {label} took {elapsed:.2f}s{Style.RESET_ALL}")
