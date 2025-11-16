import logging
import time
import uuid
from typing import Callable

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="API with Essential Middleware")


# 1. CORS Middleware - Handle Cross-Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


# 2. Trusted Host Middleware - Prevent Host Header attacks
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "*.yourdomain.com"])


# 3. GZip Middleware - Compress responses
app.add_middleware(GZipMiddleware, minimum_size=1000)


# 4. Custom Request ID Middleware - Track requests
class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response


app.add_middleware(RequestIDMiddleware)


# 5. Logging Middleware - Log all requests and responses
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()

        # Log request
        logger.info(f"Request: {request.method} {request.url.path} [ID: {getattr(request.state, 'request_id', 'N/A')}]")

        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        # Log response
        logger.info(
            f"Response: {response.status_code} [ID: {getattr(request.state, 'request_id', 'N/A')}] Time: {process_time:.4f}s"
        )

        return response


app.add_middleware(LoggingMiddleware)


# 6. Rate Limiting with SlowAPI (Production-ready)
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

# Initialize SlowAPI limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute", "1000/hour"],
    storage_uri="memory://",  # Use "redis://localhost:6379" for production
    strategy="fixed-window",  # Options: fixed-window, moving-window
)

# Add SlowAPI to app state
app.state.limiter = limiter

# Add SlowAPI middleware
app.add_middleware(SlowAPIMiddleware)


# Custom Exception Classes
class BaseAPIException(Exception):
    """Base exception for all custom API exceptions"""

    def __init__(self, message: str, status_code: int = 500, error_code: str = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or self.__class__.__name__
        super().__init__(self.message)


class ResourceNotFoundException(BaseAPIException):
    """Raised when a requested resource is not found"""

    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            message=f"{resource} with id '{resource_id}' not found", status_code=404, error_code="RESOURCE_NOT_FOUND"
        )
        self.resource = resource
        self.resource_id = resource_id


class ValidationException(BaseAPIException):
    """Raised when validation fails"""

    def __init__(self, field: str, message: str):
        super().__init__(
            message=f"Validation failed for field '{field}': {message}", status_code=422, error_code="VALIDATION_ERROR"
        )
        self.field = field


class UnauthorizedException(BaseAPIException):
    """Raised when user is not authenticated"""

    def __init__(self, message: str = "Authentication required"):
        super().__init__(message=message, status_code=401, error_code="UNAUTHORIZED")


class ForbiddenException(BaseAPIException):
    """Raised when user doesn't have permission"""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message=message, status_code=403, error_code="FORBIDDEN")


class BusinessLogicException(BaseAPIException):
    """Raised when business logic validation fails"""

    def __init__(self, message: str):
        super().__init__(message=message, status_code=400, error_code="BUSINESS_LOGIC_ERROR")


class ExternalServiceException(BaseAPIException):
    """Raised when external service fails"""

    def __init__(self, service: str, message: str):
        super().__init__(
            message=f"External service '{service}' failed: {message}", status_code=502, error_code="EXTERNAL_SERVICE_ERROR"
        )
        self.service = service


class RateLimitExceededException(BaseAPIException):
    """Raised when rate limit is exceeded"""

    def __init__(self, retry_after: int):
        super().__init__(message="Rate limit exceeded", status_code=429, error_code="RATE_LIMIT_EXCEEDED")
        self.retry_after = retry_after


class DatabaseException(BaseAPIException):
    """Raised when database operation fails"""

    def __init__(self, operation: str, message: str):
        super().__init__(message=f"Database {operation} failed: {message}", status_code=500, error_code="DATABASE_ERROR")
        self.operation = operation


# 7. Enhanced Error Handling Middleware - Handle custom exceptions
class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        try:
            response = await call_next(request)
            return response

        # Handle FastAPI HTTPException
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "success": False,
                    "error": {"code": "HTTP_EXCEPTION", "message": exc.detail},
                    "request_id": getattr(request.state, "request_id", None),
                    "path": request.url.path,
                },
            )

        # Handle custom ResourceNotFoundException
        except ResourceNotFoundException as exc:
            logger.warning(f"Resource not found: {exc.resource} - {exc.resource_id}")
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "success": False,
                    "error": {
                        "code": exc.error_code,
                        "message": exc.message,
                        "resource": exc.resource,
                        "resource_id": exc.resource_id,
                    },
                    "request_id": getattr(request.state, "request_id", None),
                    "path": request.url.path,
                },
            )

        # Handle ValidationException
        except ValidationException as exc:
            logger.warning(f"Validation error: {exc.field} - {exc.message}")
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "success": False,
                    "error": {"code": exc.error_code, "message": exc.message, "field": exc.field},
                    "request_id": getattr(request.state, "request_id", None),
                    "path": request.url.path,
                },
            )

        # Handle UnauthorizedException
        except UnauthorizedException as exc:
            logger.warning(f"Unauthorized access attempt: {request.url.path}")
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "success": False,
                    "error": {"code": exc.error_code, "message": exc.message},
                    "request_id": getattr(request.state, "request_id", None),
                    "path": request.url.path,
                },
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Handle ForbiddenException
        except ForbiddenException as exc:
            logger.warning(f"Forbidden access attempt: {request.url.path}")
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "success": False,
                    "error": {"code": exc.error_code, "message": exc.message},
                    "request_id": getattr(request.state, "request_id", None),
                    "path": request.url.path,
                },
            )

        # Handle ExternalServiceException
        except ExternalServiceException as exc:
            logger.error(f"External service error: {exc.service} - {exc.message}")
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "success": False,
                    "error": {"code": exc.error_code, "message": exc.message, "service": exc.service},
                    "request_id": getattr(request.state, "request_id", None),
                    "path": request.url.path,
                },
            )

        # Handle DatabaseException
        except DatabaseException as exc:
            logger.error(f"Database error: {exc.operation} - {exc.message}")
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "success": False,
                    "error": {"code": exc.error_code, "message": "A database error occurred", "operation": exc.operation},
                    "request_id": getattr(request.state, "request_id", None),
                    "path": request.url.path,
                },
            )

        # Handle RateLimitExceededException (Custom)
        except RateLimitExceededException as exc:
            logger.warning(f"Rate limit exceeded for {request.client.host}")
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "success": False,
                    "error": {"code": exc.error_code, "message": exc.message, "retry_after": exc.retry_after},
                    "request_id": getattr(request.state, "request_id", None),
                    "path": request.url.path,
                },
                headers={"Retry-After": str(exc.retry_after)},
            )

        # Handle SlowAPI RateLimitExceeded
        except RateLimitExceeded as exc:
            logger.warning(f"SlowAPI rate limit exceeded for {request.client.host}")
            # Extract retry_after from the exception if available
            retry_after = getattr(exc, "retry_after", 60)
            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": "Too many requests. Please slow down.",
                        "retry_after": retry_after,
                    },
                    "request_id": getattr(request.state, "request_id", None),
                    "path": request.url.path,
                },
                headers={"Retry-After": str(retry_after)},
            )

        # Handle any custom BaseAPIException
        except BaseAPIException as exc:
            logger.error(f"API Exception: {exc.error_code} - {exc.message}")
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "success": False,
                    "error": {"code": exc.error_code, "message": exc.message},
                    "request_id": getattr(request.state, "request_id", None),
                    "path": request.url.path,
                },
            )

        # Handle unexpected exceptions
        except Exception as exc:
            logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "error": {"code": "INTERNAL_SERVER_ERROR", "message": "An unexpected error occurred"},
                    "request_id": getattr(request.state, "request_id", None),
                    "path": request.url.path,
                },
            )


app.add_middleware(ErrorHandlingMiddleware)


# 8. Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security-related HTTP headers to responses."""

    async def dispatch(self, request: Request, call_next: Callable):
        response = await call_next(request)  # call_next(request) processes the request and returns the downstream Response
        # prevents MIME type sniffing; forces browser to respect declared Content-Type
        response.headers["X-Content-Type-Options"] = "nosniff"
        # disallows embedding the page in frames/iframes to prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"
        # enables browser XSS protection and blocks rendering if an attack is detected
        response.headers["X-XSS-Protection"] = "1; mode=block"
        # enforces HTTPS for 1 year and includes all subdomains
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        # restricts resource loading to the same origin by default
        response.headers["Content-Security-Policy"] = "default-src 'self'"

        return response  # return the modified response with security headers applied


app.add_middleware(SecurityHeadersMiddleware)


# Sample Endpoints with Custom Exception Examples
@app.get("/")
@limiter.limit("10/minute")  # Override default limit for this endpoint
async def root(request: Request):
    return {"message": "API with comprehensive middleware"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/items/{item_id}")
@limiter.limit("50/minute")  # Custom limit for this endpoint
async def get_item(item_id: int, request: Request):
    # Simulate resource not found
    if item_id == 999:
        raise ResourceNotFoundException(resource="Item", resource_id=str(item_id))

    # Simulate validation error
    if item_id < 0:
        raise ValidationException(field="item_id", message="Item ID must be positive")

    return {"item_id": item_id, "request_id": request.state.request_id}


@app.post("/items")
@limiter.limit("20/minute")  # Stricter limit for POST operations
async def create_item(item: dict, request: Request):
    # Simulate business logic validation
    if not item.get("name"):
        raise ValidationException(field="name", message="Name is required")

    if len(item.get("name", "")) < 3:
        raise BusinessLogicException("Item name must be at least 3 characters long")

    return {"created": True, "item": item}


@app.get("/error")
async def trigger_error():
    raise HTTPException(status_code=400, detail="This is a test error")


@app.get("/protected")
async def protected_route():
    """This endpoint requires API key if APIKeyMiddleware is enabled"""
    # Simulate authentication check
    # raise UnauthorizedException("Please provide valid credentials")
    return {"message": "This is a protected resource"}


@app.get("/admin")
async def admin_route():
    """Simulate authorization check"""
    # Check if user has admin role (simulated)
    is_admin = False
    if not is_admin:
        raise ForbiddenException("Admin access required")

    return {"message": "Admin data"}


@app.get("/external")
async def call_external_service():
    """Simulate external service call"""
    # Simulate external service failure
    service_available = False
    if not service_available:
        raise ExternalServiceException(service="PaymentGateway", message="Connection timeout")

    return {"data": "from external service"}


@app.get("/database")
async def database_operation():
    """Simulate database operation"""
    # Simulate database error
    db_error = True
    if db_error:
        raise DatabaseException(operation="SELECT", message="Connection pool exhausted")

    return {"data": "from database"}


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """Example with multiple exception scenarios"""
    # Validate user_id format
    if not user_id.isalnum():
        raise ValidationException(field="user_id", message="User ID must be alphanumeric")

    # Check if user exists
    user_exists = False  # Simulate database check
    if not user_exists:
        raise ResourceNotFoundException(resource="User", resource_id=user_id)

    return {"user_id": user_id, "name": "John Doe"}


# Endpoint to test rate limiting specifically
@app.get("/limited")
@limiter.limit("5/minute")  # Very strict limit for testing
async def limited_endpoint(request: Request):
    return {"message": "This endpoint is heavily rate limited", "request_id": request.state.request_id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
