from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.models.portfolio import Portfolio
from app.repositories.base import BaseRepository


class PortfolioRepository(BaseRepository[Portfolio]):

    def __init__(self):
        super().__init__(Portfolio)

    # -------------------------------------------------
    # GET ALL BY USER
    # -------------------------------------------------

    def get_all_by_user(
        self,
        db: Session,
        user_id: int,
        page: int,
        size: int,
        search: str | None,
        sort: str,
        order: str,
    ):
        query = db.query(Portfolio).filter(
            Portfolio.user_id == user_id
        )

        if search:
            query = query.filter(
                Portfolio.name.ilike(f"%{search}%")
            )

        total = query.count()

        sort_column = getattr(
            Portfolio,
            sort,
            Portfolio.id,
        )

        if order.lower() == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        items = (
            query.offset((page - 1) * size)
            .limit(size)
            .all()
        )

        return {
            "page": page,
            "size": size,
            "total": total,
            "pages": (total + size - 1) // size,
            "items": items,
        }

    # -------------------------------------------------
    # GET BY ID AND USER
    # -------------------------------------------------

    def get_by_id_and_user(
        self,
        db: Session,
        portfolio_id: int,
        user_id: int,
    ):
        return (
            db.query(Portfolio)
            .filter(
                Portfolio.id == portfolio_id,
                Portfolio.user_id == user_id,
            )
            .first()
        )

    # -------------------------------------------------
    # GET BY NAME
    # -------------------------------------------------

    def get_by_name(
        self,
        db: Session,
        user_id: int,
        name: str,
    ):
        return (
            db.query(Portfolio)
            .filter(
                Portfolio.user_id == user_id,
                Portfolio.name == name,
            )
            .first()
        )

    # -------------------------------------------------
    # NAME EXISTS FOR OTHER
    # -------------------------------------------------

    def name_exists_for_other(
        self,
        db: Session,
        portfolio_id: int,
        user_id: int,
        name: str,
    ):
        return (
            db.query(Portfolio)
            .filter(
                Portfolio.id != portfolio_id,
                Portfolio.user_id == user_id,
                Portfolio.name == name,
            )
            .first()
        )

    # -------------------------------------------------
    # GET DEFAULT
    # -------------------------------------------------

    def get_default(
        self,
        db: Session,
        user_id: int,
    ):
        return (
            db.query(Portfolio)
            .filter(
                Portfolio.user_id == user_id,
                Portfolio.is_default.is_(True),
            )
            .first()
        )