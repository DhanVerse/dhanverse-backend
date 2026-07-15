from pydantic import BaseModel, Field, field_validator


class CompanyBase(BaseModel):
    symbol: str = Field(
        ...,
        min_length=2,
        max_length=20,
        description="Stock Symbol"
    )

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Company Name"
    )

    sector: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    industry: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    isin: str = Field(
        ...,
        min_length=12,
        max_length=12,
        description="ISIN Number"
    )

    description: str = Field(
        ...,
        min_length=5,
        max_length=500
    )

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, value: str):
        value = value.strip().upper()

        if not value.isalnum():
            raise ValueError(
                "Symbol must contain only letters and numbers."
            )

        return value

    @field_validator("isin")
    @classmethod
    def validate_isin(cls, value: str):

        value = value.strip().upper()

        if len(value) != 12:
            raise ValueError(
                "ISIN must contain exactly 12 characters."
            )

        if not value[:2].isalpha():
            raise ValueError(
                "ISIN must begin with a country code."
            )

        return value

    @field_validator(
        "name",
        "sector",
        "industry",
        "description"
    )
    @classmethod
    def remove_extra_spaces(cls, value: str):
        return value.strip()


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    pass


class CompanyResponse(CompanyBase):
    id: int

    class Config:
        from_attributes = True


class CompanyListResponse(BaseModel):
    page: int
    size: int
    total: int
    pages: int
    items: list[CompanyResponse]