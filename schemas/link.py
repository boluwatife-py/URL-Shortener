from pydantic import BaseModel, HttpUrl
from datetime import datetime

class LinkCreate(BaseModel):
    title: str
    url: HttpUrl

class LinkResponse(BaseModel):
    id: str
    title: str
    url: HttpUrl
    shortened_url: HttpUrl
    created_at: datetime
