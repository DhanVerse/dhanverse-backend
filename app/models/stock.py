from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class Stock(Base):
    __tablename__ = "stocks"

    __table_args__ = (
        UniqueConstraint(
            "exchange",
            "trading_symbol",
            name="uq_stock_exchange_symbol",
        ),
    )

    # ---------------------------------------------------------
    # Primary Key
    # ---------------------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ---------------------------------------------------------
    # Company Relationship
    # One Company -> Many Stock Listings
    # ---------------------------------------------------------

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # Exchange Information
    # ---------------------------------------------------------

    exchange = Column(
        String(20),
        nullable=False,
        index=True,
    )

    trading_symbol = Column(
        String(30),
        nullable=False,
        index=True,
    )

    exchange_symbol = Column(
        String(30),
        nullable=True,
    )

    series = Column(
        String(10),
        default="EQ",
        nullable=False,
    )

    # ---------------------------------------------------------
    # Instrument Information
    # ---------------------------------------------------------

    instrument_type = Column(
        String(30),
        default="EQUITY",
        nullable=False,
        index=True,
    )

    market_segment = Column(
        String(30),
        default="CASH",
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # Trading Details
    # ---------------------------------------------------------

    lot_size = Column(
        Integer,
        default=1,
        nullable=False,
    )

    tick_size = Column(
        Float,
        default=0.05,
        nullable=False,
    )

    face_value = Column(
        Float,
        default=10.0,
        nullable=False,
    )

    listed = Column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # Audit Fields
    # ---------------------------------------------------------

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company = relationship(
        "Company",
        back_populates="stocks",
    )