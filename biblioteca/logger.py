# logger.py
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

DEFAULT_LOGFILE = "scriptlang.log"
_logger: Optional[logging.Logger] = None

def init_logger(logfile: str = DEFAULT_LOGFILE, level: str = "INFO",
                max_bytes: int = 5 * 1024 * 1024, backup_count: int = 3) -> logging.Logger:
    global _logger
    if _logger:
        _logger.setLevel(level.upper())
        return _logger

    p = Path(logfile)
    p.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("scriptlang")
    logger.setLevel(level.upper())

    handler = RotatingFileHandler(str(p), maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
    fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(fmt)
    logger.addHandler(handler)

    # consola (útil en desarrollo)
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.addHandler(console)

    logger.propagate = False
    _logger = logger
    return _logger

def get_logger() -> logging.Logger:
    if _logger is None:
        return init_logger()
    return _logger

def log_info(msg: str):
    get_logger().info(msg)

def log_debug(msg: str):
    get_logger().debug(msg)

def log_warning(msg: str):
    get_logger().warning(msg)

def log_error(msg: str, exc_info: bool = False):
    get_logger().error(msg, exc_info=exc_info)
