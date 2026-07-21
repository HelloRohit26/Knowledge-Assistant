"""
FastAPI Request Logging & Timing Middleware
"""

import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.logger import logger
from app.core.metrics import metrics


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        try:
            response = await call_next(request)
            duration_ms = (time.time() - start_time) * 1000

            is_error = response.status_code >= 400
            metrics.record_request(duration_ms, is_error=is_error)

            logger.info(
                f"{request.method} {request.url.path} "
                f"- Status: {response.status_code} - Duration: {duration_ms:.2f}ms"
            )

            response.headers["X-Process-Time-MS"] = f"{duration_ms:.2f}"
            return response

        except Exception as exc:
            duration_ms = (time.time() - start_time) * 1000
            metrics.record_request(duration_ms, is_error=True)
            logger.error(
                f"Unhandled Exception on {request.method} {request.url.path}: {exc}",
                exc_info=True
            )
            raise exc
