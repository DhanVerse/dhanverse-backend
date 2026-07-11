from sqlalchemy.orm import Session

from app.models.company import Company
from app.repositories.company import CompanyRepository
from app.schemas.company import CompanyCreate


class CompanyService:

    def __init__(self):
        self.repo = CompanyRepository()

    def get_all(self, db: Session):
        return self.repo.get_all(db)

    def get_by_id(self, db: Session, company_id: int):
        return self.repo.get_by_id(
            db=db,
            company_id=company_id
        )

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