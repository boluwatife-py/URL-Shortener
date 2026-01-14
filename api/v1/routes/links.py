from fastapi import APIRouter, Depends
from pydantic import HttpUrl
from core.config import settings
from schemas.link import LinkCreate, LinkResponse
from services.link_service import LinkService, get_link_service

router = APIRouter(prefix="/links", tags=["links"])


@router.post("/", response_model=LinkResponse)
async def create_link_route(data: LinkCreate, service: LinkService = Depends(get_link_service)):
    link = await service.create_link(title=data.title, url=data.url)
    return LinkResponse(
        id=link.public_id,
        title=link.title,
        url=HttpUrl(link.url),
        shortened_url=HttpUrl(f"{settings.HOST_URL}/{link.public_id}"),
        created_at=link.created_at
    )


@router.get("/", response_model=list[LinkResponse])
async def list_links(service: LinkService = Depends(get_link_service)):
    links = await service.get_links()
    return [
        LinkResponse(
            id=l.public_id,
            title=l.title,
            url=HttpUrl(l.url),
            shortened_url=HttpUrl(f"{settings.HOST_URL}/{l.public_id}"),
            created_at=l.created_at
        )
        for l in links
    ]


@router.get("/{link_id}", response_model=LinkResponse)
async def read_link(link_id: str, service: LinkService = Depends(get_link_service)):
    link = await service.get_link(link_id)
    return LinkResponse(
        id=link.public_id,
        title=link.title,
        url=HttpUrl(link.url),
        shortened_url=HttpUrl(f"{settings.HOST_URL}/{link.public_id}"),
        created_at=link.created_at
    )


@router.put("/{link_id}", response_model=LinkResponse)
async def update_link_route(link_id: str, data: LinkCreate, service: LinkService = Depends(get_link_service)):
    link = await service.update_link(link_id, title=data.title, url=data.url)
    return LinkResponse(
        id=link.public_id,
        title=link.title,
        url=HttpUrl(link.url),
        shortened_url=HttpUrl(f"{settings.HOST_URL}/{link.public_id}"),
        created_at=link.created_at
    )


@router.delete("/{link_id}")
async def delete_link_route(link_id: str, service: LinkService = Depends(get_link_service)):
    await service.delete_link(link_id)
    return {"detail": "Link deleted"}