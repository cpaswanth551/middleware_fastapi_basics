
from collections import defaultdict
import time
from typing import Dict
from fastapi import FastAPI, Request, status
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    DispatchFunction,
    RequestResponseEndpoint,
)
from starlette.responses import Response
from starlette.types import ASGIApp


class AdvancedMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.rate_limit_records: Dict[str, float] = defaultdict(float)

    async def log_message(self, message: str):
        print(message)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        if current_time - self.rate_limit_records[client_ip] < 5:
            return Response(
                content="Rate Limit exceeded.",
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        self.rate_limit_records[client_ip] = current_time

        path = request.url.path
        await self.log_message(f"Request to {path}")

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # add custom header

        custom_headers = {"X-Process-Time": str(process_time)}

        for header, value in custom_headers.items():
            response.headers.append(header, value)

        await self.log_message(f"response for {path} took {process_time} second")

        return response
