
import time
import asyncio
from collections import deque
from typing import Dict, Optional, Tuple

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from core.utils.config import settings


class RateLimiter:
    def __init__(self, limit: int = 100, window: int = 60):
        self.limit = limit
        self.window = window
        self.storage: Dict[str, deque] = {}
        self.lock = asyncio.Lock()

    async def is_allowed(self, key: str, limit: Optional[int] = None, window: Optional[int] = None) -> Tuple[bool, int, int]:
        
        if limit is None:
            limit = self.limit
        if window is None:
            window = self.window

        now = time.time()
        async with self.lock:
            dq = self.storage.setdefault(key, deque())
            while dq and dq[0] <= now - window:
                dq.popleft()
            if len(dq) < limit:
                dq.append(now)
                remaining = limit - len(dq)
                reset = int(window - (now - dq[0])) if dq else window
                return True, remaining, max(reset, 0)
            else:
                remaining = 0
                reset = int(window - (now - dq[0])) if dq else window
                return False, remaining, max(reset, 0)


global_limiter = RateLimiter(settings.RATE_LIMIT_REQUESTS, settings.RATE_LIMIT_WINDOW_SECONDS)


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limiter: Optional[RateLimiter] = None, enabled: bool = True):
        super().__init__(app)
        self.limiter = limiter or global_limiter
        self.enabled = enabled

    async def dispatch(self, request: Request, call_next):
        if not self.enabled:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        allowed, remaining, reset = await self.limiter.is_allowed(client_ip)
        if not allowed:
            from fastapi.responses import JSONResponse

            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"},
                headers={
                    "X-RateLimit-Limit": str(self.limiter.limit),
                    "X-RateLimit-Remaining": str(remaining),
                    "Retry-After": str(reset),
                },
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.limiter.limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(reset)
        return response


def rate_limit_dependency(limit: Optional[int] = None, window: Optional[int] = None):
    async def dependency(request: Request):
        client_ip = request.client.host if request.client else "unknown"
        allowed, remaining, reset = await global_limiter.is_allowed(client_ip, limit, window)
        if not allowed:
            from fastapi import HTTPException, status

            raise HTTPException(status_code=429, detail="Rate limit exceeded")

    return dependency
