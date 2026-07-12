from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.company import Company


class CompanyRepository:

    def get_all(self, db: Session):
        return db.query(Company).all()

    def search(
        self,
        db: Session,
        keyword: str,
    ):
        return (
            db.query(Company)
            .filter(
                or_(
                    Company.name.ilike(f"%{keyword}%"),
                    Company.symbol.ilike(f"%{keyword}%")
                )
            )
            .all()
        )

    def get_by_id(self, db: Session, company_id: int):
        return (
            db.query(Company)
            .filter(Company.id == company_id)
            .first()
        )

    def create(
        self,
        db: Session,
        company: Company,
    ):
        db.add(company)
        db.commit()
        db.refresh(company)
        return company

    def update(
        self,
        db: Session,
        company: Company,
        data: dict,
    ):
        for key, value in data.items():
            setattr(company, key, value)

        db.commit()
        db.refresh(company)

        return company

    def delete(
        self,
        db: Session,
        company: Company,
    ):
        db.delete(company)
        db.commit()