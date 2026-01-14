from datetime import datetime
from typing import List
from pydantic import BaseModel, HttpUrl


class ClickPerDay(BaseModel):
    day: datetime
    clicks: int


class ClickBySource(BaseModel):
    source: str
    clicks: int


class LinkAnalyticsResponse(BaseModel):
    url: HttpUrl
    shortended_url: HttpUrl
    total_clicks: int
    clicks_per_day: List[ClickPerDay]
    clicks_by_source: List[ClickBySource]


class AllLinksAnalyticsResponse(BaseModel):
    links: List[LinkAnalyticsResponse]
