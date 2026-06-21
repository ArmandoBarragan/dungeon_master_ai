from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies import get_auth_service
from src.schemas import TokenResponse, UserCreate, UserLogin, UserResponse
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        user, access_token = auth_service.register(
            name=payload.name,
            email=payload.email,
            password=payload.password,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        user, access_token = auth_service.login(
            email=payload.email,
            password=payload.password,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user),
    )
