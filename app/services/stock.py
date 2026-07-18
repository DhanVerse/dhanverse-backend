from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.stock import Stock
from app.repositories.stock import StockRepository
from app.schemas.stock import StockCreate, StockUpdate


class StockService:

    def __init__(self):
        self.repo = StockRepository()

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
        stock_id: int,
    ):
        stock = self.repo.get_by_id(
            db=db,
            entity_id=stock_id,
        )

        if not stock:
            raise HTTPException(
                status_code=404,
                detail="Stock not found",
            )

        return stock

    # -------------------------------------------------
    # CREATE
    # -------------------------------------------------

    def create(
        self,
        db: Session,
        stock: StockCreate,
    ):

        existing = self.repo.get_by_trading_symbol(
            db=db,
            exchange=stock.exchange,
            trading_symbol=stock.trading_symbol,
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Trading symbol already exists for this exchange",
            )

        db_stock = Stock(
            company_id=stock.company_id,
            exchange=stock.exchange,
            trading_symbol=stock.trading_symbol,
            exchange_symbol=stock.exchange_symbol,
            series=stock.series,
            instrument_type=stock.instrument_type,
            market_segment=stock.market_segment,
            lot_size=stock.lot_size,
            tick_size=stock.tick_size,
            face_value=stock.face_value,
            listed=stock.listed,
        )

        return self.repo.create(
            db=db,
            entity=db_stock,
        )

    # -------------------------------------------------
    # UPDATE
    # -------------------------------------------------

    def update(
        self,
        db: Session,
        stock_id: int,
        stock: StockUpdate,
    ):

        db_stock = self.repo.get_by_id(
            db=db,
            entity_id=stock_id,
        )

        if not db_stock:
            raise HTTPException(
                status_code=404,
                detail="Stock not found",
            )

        if self.repo.trading_symbol_exists_for_other(
            db=db,
            stock_id=stock_id,
            exchange=stock.exchange,
            trading_symbol=stock.trading_symbol,
        ):
            raise HTTPException(
                status_code=400,
                detail="Trading symbol already exists for this exchange",
            )

        return self.repo.update(
            db=db,
            entity=db_stock,
            data=stock.model_dump(exclude_unset=True),
        )

    # -------------------------------------------------
    # DELETE
    # -------------------------------------------------

    def delete(
        self,
        db: Session,
        stock_id: int,
    ):

        db_stock = self.repo.get_by_id(
            db=db,
            entity_id=stock_id,
        )

        if not db_stock:
            raise HTTPException(
                status_code=404,
                detail="Stock not found",
            )

        self.repo.delete(
            db=db,
            entity=db_stock,
        )

        return {
            "message": "Stock deleted successfully"
        }