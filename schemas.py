from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str


class CompanyRequest(CompanyBase):
    ...


class CompanyResponse(CompanyBase):
    id: int

    class Config:
        orm_mode = True
