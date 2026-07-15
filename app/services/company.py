from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.company import Company
from app.repositories.company import CompanyRepository
from app.schemas.company import CompanyCreate, CompanyUpdate


class CompanyService:

    def __init__(self):
        self.repo = CompanyRepository()

    # -------------------------------------------------
    # GET ALL
    # -------------------------------------------------

    def get_all(
        self,
        db: Session,
        page: int,
        size: int,
        search: str | None,
        sort: str,
        order: str,
    ):
        return self.repo.get_all(
            db=db,
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
        company_id: int,
    ):
        company = self.repo.get_by_id(
            db=db,
            entity_id=company_id,
        )

        if not company:
            raise HTTPException(
                status_code=404,
                detail="Company not found",
            )

        return company

    # -------------------------------------------------
    # CREATE
    # -------------------------------------------------

    def create(
        self,
        db: Session,
        company: CompanyCreate,
    ):
        if self.repo.get_by_symbol(
            db,
            company.symbol,
        ):
            raise HTTPException(
                status_code=400,
                detail="Company symbol already exists",
            )

        if self.repo.get_by_isin(
            db,
            company.isin,
        ):
            raise HTTPException(
                status_code=400,
                detail="Company ISIN already exists",
            )

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
            entity=db_company,
        )

    # -------------------------------------------------
    # UPDATE
    # -------------------------------------------------

    def update(
        self,
        db: Session,
        company_id: int,
        company: CompanyUpdate,
    ):
        db_company = self.repo.get_by_id(
            db=db,
            entity_id=company_id,
        )

        if not db_company:
            raise HTTPException(
                status_code=404,
                detail="Company not found",
            )

        if self.repo.symbol_exists_for_other(
            db=db,
            company_id=company_id,
            symbol=company.symbol,
        ):
            raise HTTPException(
                status_code=400,
                detail="Company symbol already exists",
            )

        if self.repo.isin_exists_for_other(
            db=db,
            company_id=company_id,
            isin=company.isin,
        ):
            raise HTTPException(
                status_code=400,
                detail="Company ISIN already exists",
            )

        return self.repo.update(
            db=db,
            entity=db_company,
            data=company.model_dump(),
        )

    # -------------------------------------------------
    # DELETE
    # -------------------------------------------------

    def delete(
        self,
        db: Session,
        company_id: int,
    ):
        db_company = self.repo.get_by_id(
            db=db,
            entity_id=company_id,
        )

        if not db_company:
            raise HTTPException(
                status_code=404,
                detail="Company not found",
            )

        self.repo.delete(
            db=db,
            entity=db_company,
        )

        return {
            "message": "Company deleted successfully"
        }