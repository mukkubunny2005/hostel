import logging, os
from logging.handlers import TimedRotatingFileHandler
from core.secure_logger import formatter
DIR = "secure_logs/audit"
os.makedirs(DIR, exist_ok=True)

def get_audit_logger():
    logger = logging.getLogger("AUDIT")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler(
        f"{DIR}/audit.log", when="h", backupCount=180
    )
    handler.setFormatter(logging.Formatter(formatter))
    logger.addHandler(handler)
    logger.propagate = False
    return logger

