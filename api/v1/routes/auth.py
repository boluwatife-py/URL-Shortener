from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from services.auth_service import register_user, authenticate_user
from schemas.auth import RegisterRequest, LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=LoginResponse)
async def register(data: RegisterRequest, response: Response, db: AsyncSession = Depends(get_db)):
    user = await register_user(db, data.email, data.password)
    access, refresh, public_id = await authenticate_user(db, data.email, data.password)

    response.set_cookie(
        "refresh_token",
        refresh,
        httponly=True,
        samesite="lax",
        secure=False
    )

    return LoginResponse(access_token=access, email=data.email, id=public_id)


@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    access, refresh, public_id = await authenticate_user(db, data.email, data.password)

    response.set_cookie(
        "refresh_token",
        refresh,
        httponly=True,
        samesite="lax",
        secure=False
    )

    return LoginResponse(access_token=access, email=data.email, id=public_id)
