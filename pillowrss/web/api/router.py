from fastapi.routing import APIRouter

from pillowrss.web.api import monitoring, rss

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(rss.router, tags=["rss"])
