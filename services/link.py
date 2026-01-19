from typing import Optional
from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException
from models.link import Link
from core.utils.hashid import HashID
from core.database import get_db
from models.user import User
from services.auth import get_current_user


class LinkService:
    def __init__(self, db: AsyncSession, user: User):
        self.db = db
        self.user = user

    async def create_link(self, title: str, url: HttpUrl) -> Link:
        new_link = Link(user_id=self.user.id, title=title, url=str(url))
        self.db.add(new_link)
        await self.db.commit()
        await self.db.refresh(new_link)
        return new_link

    async def get_links(self):
        result = await self.db.execute(select(Link).where(Link.user_id == self.user.id))
        return result.scalars().all()

    async def get_link(self, link_id: str) -> Link:
        result = await self.db.execute(
            select(Link).where(Link.user_id == self.user.id, Link.id == HashID.decode(link_id))
        )
        link = result.scalar_one_or_none()
        if not link:
            raise HTTPException(status_code=404, detail="Link not found")
        return link

    async def update_link(self, link_id: str, title: Optional[str] = None, url: Optional[HttpUrl] = None) -> Link:
        link = await self.get_link(link_id)
        if title:
            link.title = title
        if url:
            link.url = str(url)
        await self.db.commit()
        await self.db.refresh(link)
        return link

    async def delete_link(self, link_id: str):
        link = await self.get_link(link_id)
        await self.db.delete(link)
        await self.db.commit()



async def get_link_service(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
) -> LinkService:
    return LinkService(db, user)
