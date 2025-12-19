import magic
from fastapi import HTTPException, UploadFile, status
from core.config import MAX_fILE_SIZE, ALLOWED_MIME_TIPES
async def validate_file_security(file:UploadFile):
    size = 0
    while chunk := await file.read(1024 * 1024):
        size += len(chunk)
        if size > MAX_fILE_SIZE:
            raise HTTPException(status_code=status.HTTP_413_CONTENT_TOO_LARGE, detail='File is too large')
        await file.seek(0)
        header = await file.read(2048)
        actual_mime_type = magic.from_buffer(header, mime=True)
        await file.seek(0)
        if actual_mime_type not in ALLOWED_MIME_TIPES:
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=f'invalid file content. Type {actual_mime_type} is not allowed')
        if file.content_type != actual_mime_type :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='File meta data mismatch. Content does not match')
        return file