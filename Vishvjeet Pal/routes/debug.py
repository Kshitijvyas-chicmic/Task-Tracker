from fastapi import APIRouter, Depends

from core.utils.rate_limiter import rate_limit_dependency

router = APIRouter(prefix="/debug", tags=["debug"])


@router.get("/ratelimit")
async def rate_limit_test(dep=Depends(rate_limit_dependency(limit=5, window=1))):
    return {"ok": True}
