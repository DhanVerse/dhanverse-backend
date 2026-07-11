from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.auth import (
    UserRegister,
    UserResponse,
    UserLogin
)
from app.services.auth import AuthService
from app.core.jwt import create_access_token
from app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

auth_service = AuthService()


@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    try:
        return auth_service.register(
            db=db,
            user=user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    try:

        logged_user = auth_service.login(
            db=db,
            email=user.email,
            password=user.password
        )

        token = create_access_token(
            {
                "sub": logged_user.email
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get(
    "/me",
    response_model=UserResponse
)
def me(
    current_user=Depends(get_current_user)
):
    return current_user