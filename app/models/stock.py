from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        unique=True,
        nullable=False,
    )

    exchange = Column(
        String,
        nullable=False,
    )

    trading_symbol = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    bse_symbol = Column(
        String,
        nullable=True,
    )

    lot_size = Column(
        Integer,
        default=1,
    )

    tick_size = Column(
        Float,
        default=0.05,
    )

    face_value = Column(
        Float,
        default=10,
    )

    listed = Column(
        Boolean,
        default=True,
    )

    company = relationship(
        "Company",
        back_populates="stock",
    )