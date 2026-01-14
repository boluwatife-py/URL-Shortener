from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from fastapi import HTTPException
from models.link import Link, LinkEvent
from models.user import User
from core.utils.hashid import HashID
from schemas.analytics import LinkAnalyticsResponse, ClickPerDay, ClickBySource, AllLinksAnalyticsResponse
from pydantic import HttpUrl
from core.config import settings

class AnalyticsService:
    def __init__(self, db: AsyncSession, user: User):
        self.db = db
        self.user = user
        

    async def get_link_analytics(self, public_id: str) -> LinkAnalyticsResponse:
        link_id = HashID.decode(public_id)
        result = await self.db.execute(
            select(Link).where(Link.id == link_id, Link.user_id == self.user.id)
        )

        link = result.scalar_one_or_none()
        if not link:
            raise HTTPException(status_code=404, detail="Link not found")


        total_clicks = await self.db.scalar(
            select(func.count()).where(LinkEvent.link_id == link.id)
        )

        total_clicks = total_clicks or 0


        clicks_per_day_result = await self.db.execute(
            select(
                func.date_trunc("day", LinkEvent.clicked_at).label("day"),
                func.count().label("clicks")
            )
            .where(LinkEvent.link_id == link.id)
            .group_by("day")
            .order_by("day")
        )

        clicks_per_day = [ClickPerDay(day=r.day, clicks=r.clicks) for r in clicks_per_day_result.all()]


        clicks_by_source_result = await self.db.execute(
            select(
                LinkEvent.source,
                func.count().label("clicks")
            )
            .where(LinkEvent.link_id == link.id)
            .group_by(LinkEvent.source)
        )

        clicks_by_source = [ClickBySource(source=r.source or "unknown", clicks=r.clicks) for r in clicks_by_source_result.all()]

        return LinkAnalyticsResponse(
            shortended_url=HttpUrl(f"{settings.HOST_URL}/{link.public_id}"),
            url=HttpUrl(link.url),
            total_clicks=total_clicks,
            clicks_per_day=clicks_per_day,
            clicks_by_source=clicks_by_source
        )

    async def get_all_links_analytics(self) -> AllLinksAnalyticsResponse:
        result = await self.db.execute(select(Link).where(Link.user_id == self.user.id))
        links = result.scalars().all()
        
        if not links:
            return AllLinksAnalyticsResponse(links=[])

        analytics = []
        for link in links:
            link_data = await self.get_link_analytics(link.public_id)
            analytics.append(link_data)

        return AllLinksAnalyticsResponse(links=analytics)
