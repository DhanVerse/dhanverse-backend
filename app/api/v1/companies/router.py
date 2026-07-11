from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.company import CompanyCreate, CompanyResponse
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
    db: Session = Depends(get_db)
):
    return company_service.create(
        db=db,
        company=company
    )