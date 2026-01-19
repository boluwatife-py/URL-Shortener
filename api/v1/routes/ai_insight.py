from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from services.analytics import AnalyticsService
from services.ai_insight import AIInsightService
from services.auth import get_current_user
from models.user import User
from schemas.analytics import LinkAnalyticsResponse
from schemas.ai_insight import AIPromptRequest

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/insights")
async def generate_ai_insights(
    body: AIPromptRequest= Body(..., description="Your custom prompt for AI insights"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    analytics_service = AnalyticsService(db, user)
    all_data = await analytics_service.get_all_links_analytics()

    ai_service = AIInsightService()
    insights_text = await ai_service.generate_insights(all_data.links, user_prompt=body.prompt)

    return {"insights": insights_text}
