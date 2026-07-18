from sqlalchemy import (
    Column,
    Integer,
    String,
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class Company(Base):
    __tablename__ = "companies"

    # ---------------------------------------------------------
    # Primary Key
    # ---------------------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ---------------------------------------------------------
    # Company Information
    # ---------------------------------------------------------

    symbol = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    name = Column(
        String(100),
        nullable=False,
        index=True,
    )

    sector = Column(
        String(100),
        nullable=False,
    )

    industry = Column(
        String(100),
        nullable=False,
    )

    isin = Column(
        String(12),
        unique=True,
        nullable=False,
        index=True,
    )

    description = Column(
        String(500),
        nullable=False,
    )

    # ---------------------------------------------------------
    # Relationships
    # One Company -> Many Stock Listings
    # ---------------------------------------------------------

    stocks = relationship(
        "Stock",
        back_populates="company",
        cascade="all, delete-orphan",
    )