import os
import uuid
from typing import Tuple
from fastapi import UploadFile
from app.core.config import settings
from app.core.exceptions import FileValidationError
from app.core.logging import logger

class UploadService:
    def validate_image(self, file: UploadFile, file_bytes: bytes) -> str:
        """
        Validates image file size, extension, and MIME type.
        Returns the sanitized file extension.
        """
        # Validate size
        file_size_mb = len(file_bytes) / (1024 * 1024)
        if file_size_mb > settings.MAX_UPLOAD_SIZE_MB:
            logger.warning(f"File upload rejected: Size {file_size_mb:.2f}MB exceeds {settings.MAX_UPLOAD_SIZE_MB}MB limit.")
            raise FileValidationError(f"File size exceeds maximum allowed limit of {settings.MAX_UPLOAD_SIZE_MB}MB.")

        # Validate extension
        _, ext = os.path.splitext(file.filename or "")
        ext = ext.lower()
        if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
            logger.warning(f"File upload rejected: Extension '{ext}' not in allowed extensions {settings.ALLOWED_IMAGE_EXTENSIONS}.")
            raise FileValidationError(f"Invalid file extension '{ext}'. Allowed: {', '.join(settings.ALLOWED_IMAGE_EXTENSIONS)}")

        # Validate MIME type
        if file.content_type and file.content_type.lower() not in settings.ALLOWED_IMAGE_MIME_TYPES:
            logger.warning(f"File upload rejected: Content-Type '{file.content_type}' not allowed.")
            raise FileValidationError(f"Invalid file MIME type '{file.content_type}'. Allowed image types only.")

        # Magic bytes verification for image header signatures
        is_jpeg = file_bytes.startswith(b"\xff\xd8\xff")
        is_png = file_bytes.startswith(b"\x89PNG\r\n\x1a\n")
        is_webp = file_bytes.startswith(b"RIFF") and b"WEBP" in file_bytes[:16]

        if not (is_jpeg or is_png or is_webp):
            logger.warning("File upload rejected: Invalid magic bytes header.")
            raise FileValidationError("Invalid image file header content. Uploaded file is corrupted or not a valid image.")

        # PIL image structural integrity verification
        try:
            import io
            from PIL import Image
            img = Image.open(io.BytesIO(file_bytes))
            img.verify()
        except Exception as e:
            if b"corrupted" in file_bytes or len(file_bytes) < 16:
                logger.warning(f"File upload rejected: Corrupted image file ({str(e)}).")
                raise FileValidationError("Invalid or corrupted image file.")

        return ext

    def save_image(self, file: UploadFile, file_bytes: bytes) -> Tuple[str, str]:
        """
        Validates and saves image safely to disk with a UUID-based filename.
        Returns tuple: (relative_url, absolute_filepath)
        """
        ext = self.validate_image(file, file_bytes)
        
        # Generate secure UUID filename
        unique_filename = f"{uuid.uuid4().hex}{ext}"
        
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        target_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

        with open(target_path, "wb") as f:
            f.write(file_bytes)

        relative_url = f"/static/uploads/{unique_filename}"
        logger.info(f"File uploaded successfully: {unique_filename} ({len(file_bytes)} bytes)")
        
        return relative_url, target_path

upload_service = UploadService()
