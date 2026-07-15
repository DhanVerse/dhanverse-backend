from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.company import Company
from app.repositories.base import BaseRepository


class CompanyRepository(BaseRepository[Company]):

    def __init__(self):
        super().__init__(Company)

    # -----------------------------
    # Company-specific methods
    # -----------------------------

    def get_by_symbol(
        self,
        db: Session,
        symbol: str,
    ):
        return (
            db.query(Company)
            .filter(Company.symbol == symbol)
            .first()
        )

    def get_by_isin(
        self,
        db: Session,
        isin: str,
    ):
        return (
            db.query(Company)
            .filter(Company.isin == isin)
            .first()
        )

    def symbol_exists_for_other(
        self,
        db: Session,
        company_id: int,
        symbol: str,
    ):
        return (
            db.query(Company)
            .filter(
                Company.symbol == symbol,
                Company.id != company_id,
            )
            .first()
        )

    def isin_exists_for_other(
        self,
        db: Session,
        company_id: int,
        isin: str,
    ):
        return (
            db.query(Company)
            .filter(
                Company.isin == isin,
                Company.id != company_id,
            )
            .first()
        )

    def search(
        self,
        db: Session,
        keyword: str,
    ):
        return (
            db.query(Company)
            .filter(
                or_(
                    Company.symbol.ilike(f"%{keyword}%"),
                    Company.name.ilike(f"%{keyword}%"),
                    Company.sector.ilike(f"%{keyword}%"),
                    Company.industry.ilike(f"%{keyword}%"),
                )
            )
            .all()
        )