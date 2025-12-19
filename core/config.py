import os
UPLOAD_DIR = 'secure_storage'
MAX_fILE_SIZE = 5 * 1024 * 1024
ALLOWED_MIME_TIPES = {
    'images/jpeg': '.jpg',
    'application/pdf' : '.pdf'
}

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)