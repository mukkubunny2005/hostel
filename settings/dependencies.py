import magic
from fastapi import HTTPException, UploadFile, status
from core.config import MAX_FILE_SIZE, ALLOWED_MIME_TYPES

async def validate_file_security(file: UploadFile):
    """
    Validates file security by checking:
    1. File size doesn't exceed MAX_FILE_SIZE
    2. Actual MIME type is in ALLOWED_MIME_TYPES
    3. Content-Type header matches actual file content
    """
    # Read entire file content
    content = await file.read()
    size = len(content)
    
    # Check file size
    if size > MAX_FILE_SIZE:
        await file.seek(0)
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE, 
            detail='File is too large'
        )
    
    # Check actual MIME type from file header
    actual_mime_type = magic.from_buffer(content[:2048], mime=True)
    
    if actual_mime_type not in ALLOWED_MIME_TYPES:
        await file.seek(0)
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 
            detail=f'Invalid file content. Type {actual_mime_type} is not allowed'
        )
    
    # Check if content-type matches actual MIME type
    if file.content_type != actual_mime_type:
        await file.seek(0)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='File metadata mismatch. Content does not match declared type'
        )
    
    # Reset file pointer for further processing
    await file.seek(0)
    return file
