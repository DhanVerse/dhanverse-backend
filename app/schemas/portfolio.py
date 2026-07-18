from pydantic import BaseModel, Field, field_validator


class PortfolioBase(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Portfolio Name"
    )

    description: str | None = Field(
        default=None,
        max_length=500,
        description="Portfolio Description"
    )

    portfolio_type: str = Field(
        default="Equity",
        min_length=2,
        max_length=50,
        description="Portfolio Type"
    )

    currency: str = Field(
        default="INR",
        min_length=3,
        max_length=10,
        description="Portfolio Currency"
    )

    is_default: bool = False

    is_active: bool = True

    @field_validator(
        "name",
        "portfolio_type",
        "currency"
    )
    @classmethod
    def strip_spaces(cls, value: str):
        return value.strip()

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, value: str):
        return value.strip().upper()

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str | None):
        if value is None:
            return value
        return value.strip()


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioUpdate(PortfolioBase):
    pass


class PortfolioResponse(PortfolioBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class PortfolioListResponse(BaseModel):
    page: int
    size: int
    total: int
    pages: int
    items: list[PortfolioResponse]