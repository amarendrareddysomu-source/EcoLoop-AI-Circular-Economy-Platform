from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger("circular_economy")

class AppException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, detail: str = None):
        self.message = message
        self.status_code = status_code
        self.detail = detail or message

class NotFoundError(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)

class AuthenticationError(AppException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)

class PermissionDeniedError(AppException):
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)

class DatabaseError(AppException):
    def __init__(self, message: str = "Database transaction failed"):
        super().__init__(message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FileValidationError(AppException):
    def __init__(self, message: str = "Invalid file upload"):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)


async def app_exception_handler(request: Request, exc: AppException):
    logger.warning(f"AppException [{exc.status_code}]: {exc.message} - Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "detail": exc.detail,
            "status_code": exc.status_code
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"ValidationError on {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "message": "Input validation failed",
            "detail": exc.errors(),
            "status_code": 422
        }
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"DatabaseError on {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "DatabaseError",
            "message": "A database error occurred during operation execution.",
            "detail": "An internal database error occurred.",
            "status_code": 500
        }
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.critical(f"Unhandled Exception on {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred.",
            "detail": "An unexpected internal server error occurred.",
            "status_code": 500
        }
    )
