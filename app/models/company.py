from sqlalchemy import Column, Integer, String, Text

from app.db.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(String(20), unique=True, nullable=False)

    name = Column(String(255), nullable=False)

    sector = Column(String(100), nullable=True)

    industry = Column(String(100), nullable=True)

    isin = Column(String(20), unique=True, nullable=True)

    description = Column(Text, nullable=True)