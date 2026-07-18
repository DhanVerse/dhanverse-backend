from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.jwt import verify_access_token
from app.db.database import get_db
from app.repositories.user import UserRepository

security = HTTPBearer()

repo = UserRepository()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    payload = verify_access_token(token)

    email = payload.get("sub")

    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload",
        )

    user = repo.get_by_email(
        db=db,
        email=email,
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user