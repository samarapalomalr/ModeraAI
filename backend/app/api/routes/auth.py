from fastapi import APIRouter, Depends, Header, HTTPException

from app.api.schemas.auth import AuthResponse, LoginRequest, RegisterRequest, UserResponse
from app.core.dependencies import get_auth_service
from app.core.exceptions import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    InvalidTokenError,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=201)
def register(body: RegisterRequest, service: AuthService = Depends(get_auth_service)):
    try:
        user, token = service.register(body.name, body.email, body.password)
    except EmailAlreadyRegisteredError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return AuthResponse(access_token=token, user=user)


@router.post("/login", response_model=AuthResponse)
def login(body: LoginRequest, service: AuthService = Depends(get_auth_service)):
    try:
        user, token = service.login(body.email, body.password)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return AuthResponse(access_token=token, user=user)


@router.get("/me", response_model=UserResponse)
def me(authorization: str = Header(default=""), service: AuthService = Depends(get_auth_service)):
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    try:
        return service.get_current_user(token)
    except (InvalidTokenError, InvalidCredentialsError) as e:
        raise HTTPException(status_code=401, detail=str(e))
