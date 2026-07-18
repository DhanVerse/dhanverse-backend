from sqlalchemy.orm import Session

from app.core.exceptions import (
    DuplicateResourceError,
    ResourceNotFoundError,
)
from app.models.portfolio import Portfolio
from app.repositories.portfolio import PortfolioRepository
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioUpdate,
)


class PortfolioService:

    def __init__(self):
        self.repo = PortfolioRepository()

    # -------------------------------------------------
    # GET ALL
    # -------------------------------------------------

    def get_all(
        self,
        db: Session,
        user_id: int,
        page: int,
        size: int,
        search: str | None,
        sort: str,
        order: str,
    ):
        return self.repo.get_all_by_user(
            db=db,
            user_id=user_id,
            page=page,
            size=size,
            search=search,
            sort=sort,
            order=order,
        )

    # -------------------------------------------------
    # GET BY ID
    # -------------------------------------------------

    def get_by_id(
        self,
        db: Session,
        portfolio_id: int,
        user_id: int,
    ):
        portfolio = self.repo.get_by_id_and_user(
            db=db,
            portfolio_id=portfolio_id,
            user_id=user_id,
        )

        if not portfolio:
            raise ResourceNotFoundError(
                "Portfolio not found"
            )

        return portfolio

    # -------------------------------------------------
    # CREATE
    # -------------------------------------------------

    def create(
        self,
        db: Session,
        user_id: int,
        portfolio: PortfolioCreate,
    ):
        if self.repo.get_by_name(
            db=db,
            user_id=user_id,
            name=portfolio.name,
        ):
            raise DuplicateResourceError(
                "Portfolio name already exists"
            )

        if portfolio.is_default:
            current_default = self.repo.get_default(
                db=db,
                user_id=user_id,
            )

            if current_default:
                current_default.is_default = False
                db.commit()
                db.refresh(current_default)

        db_portfolio = Portfolio(
            user_id=user_id,
            name=portfolio.name,
            description=portfolio.description,
            portfolio_type=portfolio.portfolio_type,
            currency=portfolio.currency,
            is_default=portfolio.is_default,
            is_active=portfolio.is_active,
        )

        return self.repo.create(
            db=db,
            entity=db_portfolio,
        )

    # -------------------------------------------------
    # UPDATE
    # -------------------------------------------------

    def update(
        self,
        db: Session,
        portfolio_id: int,
        user_id: int,
        portfolio: PortfolioUpdate,
    ):
        db_portfolio = self.repo.get_by_id_and_user(
            db=db,
            portfolio_id=portfolio_id,
            user_id=user_id,
        )

        if not db_portfolio:
            raise ResourceNotFoundError(
                "Portfolio not found"
            )

        if self.repo.name_exists_for_other(
            db=db,
            portfolio_id=portfolio_id,
            user_id=user_id,
            name=portfolio.name,
        ):
            raise DuplicateResourceError(
                "Portfolio name already exists"
            )

        if portfolio.is_default:
            current_default = self.repo.get_default(
                db=db,
                user_id=user_id,
            )

            if (
                current_default
                and current_default.id != portfolio_id
            ):
                current_default.is_default = False
                db.commit()
                db.refresh(current_default)

        return self.repo.update(
            db=db,
            entity=db_portfolio,
            data=portfolio.model_dump(),
        )

    # -------------------------------------------------
    # DELETE
    # -------------------------------------------------

    def delete(
        self,
        db: Session,
        portfolio_id: int,
        user_id: int,
    ):
        db_portfolio = self.repo.get_by_id_and_user(
            db=db,
            portfolio_id=portfolio_id,
            user_id=user_id,
        )

        if not db_portfolio:
            raise ResourceNotFoundError(
                "Portfolio not found"
            )

        self.repo.delete(
            db=db,
            entity=db_portfolio,
        )

        return {
            "message": "Portfolio deleted successfully"
        }