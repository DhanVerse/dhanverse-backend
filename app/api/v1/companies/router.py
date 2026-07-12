from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user

from app.schemas.company import (
    CompanyCreate,
    CompanyUpdate,
    CompanyResponse,
)

from app.services.company import CompanyService

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)

company_service = CompanyService()


@router.get(
    "/",
    response_model=list[CompanyResponse]
)
def get_companies(
    db: Session = Depends(get_db)
):
    return company_service.get_all(db)


@router.get(
    "/search/{keyword}",
    response_model=list[CompanyResponse]
)
def search_companies(
    keyword: str,
    db: Session = Depends(get_db)
):
    return company_service.search(
        db=db,
        keyword=keyword
    )


@router.get(
    "/{company_id}",
    response_model=CompanyResponse
)
def get_company(
    company_id: int,
    db: Session = Depends(get_db)
):
    return company_service.get_by_id(
        db=db,
        company_id=company_id
    )


@router.post(
    "/",
    response_model=CompanyResponse
)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return company_service.create(
        db=db,
        company=company
    )


@router.put(
    "/{company_id}",
    response_model=CompanyResponse
)
def update_company(
    company_id: int,
    company: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return company_service.update(
        db=db,
        company_id=company_id,
        company=company
    )


@router.delete(
    "/{company_id}"
)
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return company_service.delete(
        db=db,
        company_id=company_id
    )