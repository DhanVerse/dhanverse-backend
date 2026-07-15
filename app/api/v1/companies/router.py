from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.company import (
    CompanyCreate,
    CompanyUpdate,
    CompanyResponse,
)
from app.services.company import CompanyService

router = APIRouter(
    prefix="/companies",
    tags=["Companies"],
)

company_service = CompanyService()


# ---------------------------------------------------------
# GET ALL COMPANIES
# ---------------------------------------------------------

@router.get(
    "/",
    response_model=list[CompanyResponse],
)
def get_companies(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: str | None = None,
    sort: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
):
    return company_service.get_all(
        db=db,
        page=page,
        size=size,
        search=search,
        sort=sort,
        order=order,
    )


# ---------------------------------------------------------
# GET COMPANY BY ID
# ---------------------------------------------------------

@router.get(
    "/{company_id}",
    response_model=CompanyResponse,
)
def get_company(
    company_id: int,
    db: Session = Depends(get_db),
):
    return company_service.get_by_id(
        db=db,
        company_id=company_id,
    )


# ---------------------------------------------------------
# CREATE COMPANY
# ---------------------------------------------------------

@router.post(
    "/",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db),
):
    return company_service.create(
        db=db,
        company=company,
    )


# ---------------------------------------------------------
# UPDATE COMPANY
# ---------------------------------------------------------

@router.put(
    "/{company_id}",
    response_model=CompanyResponse,
)
def update_company(
    company_id: int,
    company: CompanyUpdate,
    db: Session = Depends(get_db),
):
    return company_service.update(
        db=db,
        company_id=company_id,
        company=company,
    )


# ---------------------------------------------------------
# DELETE COMPANY
# ---------------------------------------------------------

@router.delete(
    "/{company_id}",
)
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
):
    return company_service.delete(
        db=db,
        company_id=company_id,
    )