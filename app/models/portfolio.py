from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.sql import func

from app.db.database import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    name = Column(
        String(100),
        nullable=False,
    )

    description = Column(
        String(500),
        nullable=True,
    )

    portfolio_type = Column(
        String(50),
        nullable=False,
        default="Equity",
    )

    currency = Column(
        String(10),
        nullable=False,
        default="INR",
    )

    is_default = Column(
        Boolean,
        default=False,
    )

    is_active = Column(
        Boolean,
        default=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )