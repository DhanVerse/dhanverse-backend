from sqlalchemy.orm import Session

from app.core.exceptions import (
    BusinessValidationError,
    DuplicateResourceError,
)
from app.core.security import hash_password, verify_password
from app.repositories.user import UserRepository
from app.schemas.auth import UserRegister


class AuthService:

    def __init__(self):
        self.user_repo = UserRepository()

    def register(
        self,
        db: Session,
        user: UserRegister
    ):
        existing_user = self.user_repo.get_by_email(
            db=db,
            email=user.email
        )

        if existing_user:
            raise DuplicateResourceError(
                "Email already registered"
            )

        hashed_password = hash_password(user.password)

        return self.user_repo.create(
            db=db,
            name=user.name,
            email=user.email,
            password=hashed_password
        )

    def login(
        self,
        db: Session,
        email: str,
        password: str
    ):
        user = self.user_repo.get_by_email(
            db=db,
            email=email
        )

        if not user:
            raise BusinessValidationError(
                "Invalid email or password"
            )

        if not verify_password(
            password,
            user.hashed_password
        ):
            raise BusinessValidationError(
                "Invalid email or password"
            )

        return user