from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.company import Company
from app.repositories.company import CompanyRepository
from app.schemas.company import CompanyCreate, CompanyUpdate


class CompanyService:

    def __init__(self):
        self.repo = CompanyRepository()

    def get_all(self, db: Session):
        return self.repo.get_all(db)

    def search(
        self,
        db: Session,
        keyword: str,
    ):
        return self.repo.search(
            db=db,
            keyword=keyword
        )

    def get_by_id(
        self,
        db: Session,
        company_id: int
    ):
        company = self.repo.get_by_id(
            db=db,
            company_id=company_id
        )

        if not company:
            raise HTTPException(
                status_code=404,
                detail="Company not found"
            )

        return company

    def create(
        self,
        db: Session,
        company: CompanyCreate
    ):
        db_company = Company(
            symbol=company.symbol,
            name=company.name,
            sector=company.sector,
            industry=company.industry,
            isin=company.isin,
            description=company.description,
        )

        return self.repo.create(
            db=db,
            company=db_company
        )

    def update(
        self,
        db: Session,
        company_id: int,
        company: CompanyUpdate
    ):
        db_company = self.repo.get_by_id(
            db=db,
            company_id=company_id
        )

        if not db_company:
            raise HTTPException(
                status_code=404,
                detail="Company not found"
            )

        return self.repo.update(
            db=db,
            company=db_company,
            data=company.model_dump()
        )

    def delete(
        self,
        db: Session,
        company_id: int
    ):
        db_company = self.repo.get_by_id(
            db=db,
            company_id=company_id
        )

        if not db_company:
            raise HTTPException(
                status_code=404,
                detail="Company not found"
            )

        self.repo.delete(
            db=db,
            company=db_company
        )

        return {
            "message": "Company deleted successfully"
        }