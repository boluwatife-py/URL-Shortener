from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from services.analytics_service import AnalyticsService
from services.auth_service import get_current_user
from models.user import User
from schemas.analytics import LinkAnalyticsResponse, AllLinksAnalyticsResponse

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get(
    "/link/{public_id}",
    response_model=LinkAnalyticsResponse
)
async def link_analytics(
    public_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    service = AnalyticsService(db, user)
    return await service.get_link_analytics(public_id)



@router.get(
    "/all",
    response_model=AllLinksAnalyticsResponse
)
async def all_links_analytics(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    service = AnalyticsService(db, user)
    return await service.get_all_links_analytics()
