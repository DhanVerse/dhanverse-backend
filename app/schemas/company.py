from pydantic import BaseModel


class CompanyBase(BaseModel):
    symbol: str
    name: str
    sector: str
    industry: str
    isin: str
    description: str


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    pass


class CompanyResponse(CompanyBase):
    id: int

    class Config:
        from_attributes = True