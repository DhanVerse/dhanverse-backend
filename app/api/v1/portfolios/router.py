from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioUpdate,
    PortfolioResponse,
    PortfolioListResponse,
)
from app.services.portfolio import PortfolioService

router = APIRouter(
    prefix="/portfolios",
    tags=["Portfolios"],
)

portfolio_service = PortfolioService()


# ---------------------------------------------------------
# GET ALL PORTFOLIOS
# ---------------------------------------------------------

@router.get(
    "/",
    response_model=PortfolioListResponse,
)
def get_portfolios(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: str | None = None,
    sort: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return portfolio_service.get_all(
        db=db,
        user_id=current_user.id,
        page=page,
        size=size,
        search=search,
        sort=sort,
        order=order,
    )


# ---------------------------------------------------------
# GET PORTFOLIO BY ID
# ---------------------------------------------------------

@router.get(
    "/{portfolio_id}",
    response_model=PortfolioResponse,
)
def get_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return portfolio_service.get_by_id(
        db=db,
        portfolio_id=portfolio_id,
        user_id=current_user.id,
    )


# ---------------------------------------------------------
# CREATE PORTFOLIO
# ---------------------------------------------------------

@router.post(
    "/",
    response_model=PortfolioResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_portfolio(
    portfolio: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return portfolio_service.create(
        db=db,
        user_id=current_user.id,
        portfolio=portfolio,
    )


# ---------------------------------------------------------
# UPDATE PORTFOLIO
# ---------------------------------------------------------

@router.put(
    "/{portfolio_id}",
    response_model=PortfolioResponse,
)
def update_portfolio(
    portfolio_id: int,
    portfolio: PortfolioUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return portfolio_service.update(
        db=db,
        portfolio_id=portfolio_id,
        user_id=current_user.id,
        portfolio=portfolio,
    )


# ---------------------------------------------------------
# DELETE PORTFOLIO
# ---------------------------------------------------------

@router.delete(
    "/{portfolio_id}",
)
def delete_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return portfolio_service.delete(
        db=db,
        portfolio_id=portfolio_id,
        user_id=current_user.id,
    )