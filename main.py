from fastapi import FastAPI, Request, BackgroundTasks, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from services.link_redirect import LinkRedirectService
from api.v1 import router as v1_router
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # frontend origin
    allow_credentials=True,       # allow cookies (refresh token)
    allow_methods=["*"],          # allow all HTTP methods
    allow_headers=["*"],          # allow all headers
)

async def record_click_background(
    public_id: str,
    ip_address: str | None,
    user_agent: str | None,
    source: str | None,
    db: AsyncSession
):
    service = LinkRedirectService(db)
    link = await service.get_link_by_public_id(public_id)
    await service.record_click(link, ip_address, user_agent, source)


@app.get("/{public_id}", include_in_schema=False)
async def redirect_link(
    public_id: str,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):

    background_tasks.add_task(
        record_click_background,
        public_id=public_id,
        ip_address=request.client.host, #type: ignore
        user_agent=request.headers.get("user-agent"),
        source=request.query_params.get("utm_source"),
        db=db
    )

    service = LinkRedirectService(db)
    link = await service.get_link_by_public_id(public_id)

    return RedirectResponse(url=link.url, status_code=settings.REDIRECT_STATUS_CODE)


app.include_router(v1_router)