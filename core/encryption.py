from cryptography.fernet import Fernet
import os
KEY_FILE = "core/log.key"
def load_chipper():
    if not os.path.exists(KEY_FILE):
        with open(KEY_FILE, "wb") as f:
            f.write(Fernet.generate_key())
    return Fernet(open(KEY_FILE, "rb").read())