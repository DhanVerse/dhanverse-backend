from pydantic import BaseModel


class CompanyCreate(BaseModel):
    symbol: str
    name: str
    sector: str | None = None
    industry: str | None = None
    isin: str | None = None
    description: str | None = None


class CompanyResponse(BaseModel):
    id: int
    symbol: str
    name: str
    sector: str | None = None
    industry: str | None = None
    isin: str | None = None
    description: str | None = None

    class Config:
        from_attributes = True