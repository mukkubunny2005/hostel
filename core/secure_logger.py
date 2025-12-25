import os, logging
from core.encryption import load_chipper
cipher = load_chipper()
BASE = "secure_logs/encrypted"
os.makedirs(BASE, exist_ok=True)
class EncryptionHandler(logging.Handler):
    def __init__(self, path):
        super().__init__()
        self.path = path
    def emit(self, record):
        msg = self.format(record)
        encrypted = cipher.encrypt(msg.encode())
        with open(self.path, "ab") as f:
            f.write(encrypted + b"\n")

formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s:%(message)s', datefmt='%d/%M/%Y%I:%M:%S %P')

def get_logger(name:str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if logger.handlers:
        return logger
    path = f"{BASE}/{name}.log.enc"
    handler = EncryptionHandler(path)
    handler.setFormatter(logging.Formatter(formatter))
    logger.addHandler(handler)
    logger.propagate = False
    return logger

def hostel_logger(hostel:str):
    return get_logger(f"hostel_{hostel}")

