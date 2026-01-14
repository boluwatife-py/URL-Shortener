from fastapi import APIRouter
from api.v1.routes import auth, links, analytics, ai_insight


router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(links.router)
router.include_router(analytics.router)
router.include_router(ai_insight.router)
