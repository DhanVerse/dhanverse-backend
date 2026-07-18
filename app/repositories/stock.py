from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.models.stock import Stock
from app.repositories.base import BaseRepository


class StockRepository(BaseRepository[Stock]):

    def __init__(self):
        super().__init__(Stock)

    # ---------------------------------------------------------
    # Get by Trading Symbol
    # ---------------------------------------------------------

    def get_by_trading_symbol(
        self,
        db: Session,
        exchange: str,
        trading_symbol: str,
    ):
        return (
            db.query(Stock)
            .filter(
                Stock.exchange == exchange,
                Stock.trading_symbol == trading_symbol,
            )
            .first()
        )

    # ---------------------------------------------------------
    # Get All Stocks of a Company
    # ---------------------------------------------------------

    def get_by_company(
        self,
        db: Session,
        company_id: int,
    ):
        return (
            db.query(Stock)
            .filter(
                Stock.company_id == company_id,
            )
            .all()
        )

    # ---------------------------------------------------------
    # Duplicate Trading Symbol Check
    # ---------------------------------------------------------

    def trading_symbol_exists_for_other(
        self,
        db: Session,
        stock_id: int,
        exchange: str,
        trading_symbol: str,
    ):
        return (
            db.query(Stock)
            .filter(
                Stock.id != stock_id,
                Stock.exchange == exchange,
                Stock.trading_symbol == trading_symbol,
            )
            .first()
        )

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search(
        self,
        db: Session,
        keyword: str,
    ):
        return (
            db.query(Stock)
            .filter(
                or_(
                    Stock.trading_symbol.ilike(f"%{keyword}%"),
                    Stock.exchange_symbol.ilike(f"%{keyword}%"),
                    Stock.exchange.ilike(f"%{keyword}%"),
                    Stock.series.ilike(f"%{keyword}%"),
                    Stock.instrument_type.ilike(f"%{keyword}%"),
                    Stock.market_segment.ilike(f"%{keyword}%"),
                )
            )
            .all()
        )

    # ---------------------------------------------------------
    # Get by Exchange
    # ---------------------------------------------------------

    def get_by_exchange(
        self,
        db: Session,
        exchange: str,
    ):
        return (
            db.query(Stock)
            .filter(
                Stock.exchange == exchange,
            )
            .all()
        )

    # ---------------------------------------------------------
    # Active Stocks
    # ---------------------------------------------------------

    def get_active(
        self,
        db: Session,
    ):
        return (
            db.query(Stock)
            .filter(
                Stock.listed.is_(True),
            )
            .all()
        )

    # ---------------------------------------------------------
    # Exchange + Symbol Exists
    # ---------------------------------------------------------

    def exists(
        self,
        db: Session,
        exchange: str,
        trading_symbol: str,
    ):
        return (
            db.query(Stock)
            .filter(
                and_(
                    Stock.exchange == exchange,
                    Stock.trading_symbol == trading_symbol,
                )
            )
            .first()
        )