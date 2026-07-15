from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    name = Column(
        String,
        nullable=False,
    )

    sector = Column(
        String,
        nullable=False,
    )

    industry = Column(
        String,
        nullable=False,
    )

    isin = Column(
        String,
        unique=True,
        nullable=False,
    )

    description = Column(
        String,
        nullable=False,
    )

    # One-to-One Relationship with Stock
    stock = relationship(
        "Stock",
        back_populates="company",
        uselist=False,
    )