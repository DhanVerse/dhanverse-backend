from typing import Generic, TypeVar, Type

from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    # ----------------------------------------------------
    # GET ALL
    # ----------------------------------------------------

    def get_all(
        self,
        db: Session,
        page: int = 1,
        size: int = 10,
        search: str | None = None,
        sort: str = "id",
        order: str = "asc",
    ):

        query = db.query(self.model)

        # -----------------------------
        # Search
        # -----------------------------

        if search:

            filters = []

            for column in self.model.__table__.columns:

                try:
                    if hasattr(column.type, "length") or str(column.type).startswith("VARCHAR"):
                        filters.append(column.ilike(f"%{search}%"))
                except Exception:
                    pass

            if filters:
                query = query.filter(or_(*filters))

        # -----------------------------
        # Sorting
        # -----------------------------

        if hasattr(self.model, sort):

            column = getattr(self.model, sort)

            if order.lower() == "desc":
                query = query.order_by(desc(column))
            else:
                query = query.order_by(asc(column))

        # -----------------------------
        # Pagination
        # -----------------------------

        return query.offset((page - 1) * size).limit(size).all()

    # ----------------------------------------------------
    # GET BY ID
    # ----------------------------------------------------

    def get_by_id(
        self,
        db: Session,
        entity_id: int,
    ):
        return (
            db.query(self.model)
            .filter(self.model.id == entity_id)
            .first()
        )

    # ----------------------------------------------------
    # CREATE
    # ----------------------------------------------------

    def create(
        self,
        db: Session,
        entity,
    ):
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    # ----------------------------------------------------
    # UPDATE
    # ----------------------------------------------------

    def update(
        self,
        db: Session,
        entity,
        data: dict,
    ):
        for key, value in data.items():
            setattr(entity, key, value)

        db.commit()
        db.refresh(entity)

        return entity

    # ----------------------------------------------------
    # DELETE
    # ----------------------------------------------------

    def delete(
        self,
        db: Session,
        entity,
    ):
        db.delete(entity)
        db.commit()