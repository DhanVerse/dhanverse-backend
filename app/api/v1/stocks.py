from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.stock import (
    StockCreate,
    StockResponse,
    StockUpdate,
)
from app.services.stock import StockService

router = APIRouter(
    prefix="/stocks",
    tags=["Stocks"],
)

service = StockService()


# ---------------------------------------------------------
# GET ALL
# ---------------------------------------------------------


@router.get(
    "",
    response_model=list[StockResponse],
)
def get_all_stocks(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    sort: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
):
    return service.get_all(
        db=db,
        page=page,
        size=size,
        search=search,
        sort=sort,
        order=order,
    )


# ---------------------------------------------------------
# GET BY ID
# ---------------------------------------------------------


@router.get(
    "/{stock_id}",
    response_model=StockResponse,
)
def get_stock(
    stock_id: int,
    db: Session = Depends(get_db),
):
    return service.get_by_id(
        db=db,
        stock_id=stock_id,
    )


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------


@router.post(
    "",
    response_model=StockResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_stock(
    stock: StockCreate,
    db: Session = Depends(get_db),
):
    return service.create(
        db=db,
        stock=stock,
    )


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------


@router.put(
    "/{stock_id}",
    response_model=StockResponse,
)
def update_stock(
    stock_id: int,
    stock: StockUpdate,
    db: Session = Depends(get_db),
):
    return service.update(
        db=db,
        stock_id=stock_id,
        stock=stock,
    )


# ---------------------------------------------------------
# DELETE
# ---------------------------------------------------------


@router.delete(
    "/{stock_id}",
)
def delete_stock(
    stock_id: int,
    db: Session = Depends(get_db),
):
    return service.delete(
        db=db,
        stock_id=stock_id,
    )