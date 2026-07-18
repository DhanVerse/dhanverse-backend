from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------
# Base Schema
# ---------------------------------------------------------


class StockBase(BaseModel):
    company_id: int = Field(..., gt=0)

    exchange: str = Field(
        ...,
        min_length=2,
        max_length=20,
    )

    trading_symbol: str = Field(
        ...,
        min_length=1,
        max_length=30,
    )

    exchange_symbol: Optional[str] = Field(
        default=None,
        max_length=30,
    )

    series: str = Field(
        default="EQ",
        max_length=10,
    )

    instrument_type: str = Field(
        default="EQUITY",
        max_length=30,
    )

    market_segment: str = Field(
        default="CASH",
        max_length=30,
    )

    lot_size: int = Field(
        default=1,
        ge=1,
    )

    tick_size: float = Field(
        default=0.05,
        gt=0,
    )

    face_value: float = Field(
        default=10.0,
        gt=0,
    )

    listed: bool = True


# ---------------------------------------------------------
# Create
# ---------------------------------------------------------


class StockCreate(StockBase):
    pass


# ---------------------------------------------------------
# Update
# ---------------------------------------------------------


class StockUpdate(BaseModel):

    exchange: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=20,
    )

    trading_symbol: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=30,
    )

    exchange_symbol: Optional[str] = Field(
        default=None,
        max_length=30,
    )

    series: Optional[str] = Field(
        default=None,
        max_length=10,
    )

    instrument_type: Optional[str] = Field(
        default=None,
        max_length=30,
    )

    market_segment: Optional[str] = Field(
        default=None,
        max_length=30,
    )

    lot_size: Optional[int] = Field(
        default=None,
        ge=1,
    )

    tick_size: Optional[float] = Field(
        default=None,
        gt=0,
    )

    face_value: Optional[float] = Field(
        default=None,
        gt=0,
    )

    listed: Optional[bool] = None


# ---------------------------------------------------------
# Response
# ---------------------------------------------------------


class StockResponse(StockBase):

    id: int

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)