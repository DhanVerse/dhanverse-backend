from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError

from app.db.database import get_db
from app.core.jwt import verify_access_token
from app.repositories.user import UserRepository

security = HTTPBearer()

repo = UserRepository()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    print("\n========== JWT DEBUG ==========")
    print("TOKEN:", token)

    try:
        payload = verify_access_token(token)
        print("PAYLOAD:", payload)

        email = payload.get("sub")
        print("EMAIL:", email)

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token payload"
            )

        user = repo.get_by_email(
            db=db,
            email=email
        )

        print("USER:", user)

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        print("========== END DEBUG ==========\n")

        return user

    except JWTError as e:
        print("JWT ERROR:", e)
        raise HTTPException(
            status_code=401,
            detail=f"JWT Error: {str(e)}"
        )

    except Exception as e:
        print("GENERAL ERROR:", e)
        raise