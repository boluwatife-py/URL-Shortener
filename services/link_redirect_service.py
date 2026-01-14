from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.link import Link, LinkEvent
from core.utils.hashid import HashID


class LinkRedirectService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_link_by_public_id(self, public_id: str) -> Link:
        """Fetch a link by its public ID"""
        link_id = HashID.decode(public_id)
        if not link_id:
            raise HTTPException(status_code=404, detail="Link not found")

        result = await self.db.execute(select(Link).where(Link.id == link_id))
        link = result.scalar_one_or_none()
        if not link:
            raise HTTPException(status_code=404, detail="Link not found")
        return link

    async def record_click(
        self,
        link: Link,
        ip_address: str | None = None,
        user_agent: str | None = None,
        source: str | None = None
    ):
        """Record a click event for analytics"""
        event = LinkEvent(
            link_id=link.id,
            clicked_at=datetime.now(timezone.utc),
            ip_address=ip_address,
            user_agent=user_agent,
            source=source
        )
        self.db.add(event)
        await self.db.commit()
    
    
