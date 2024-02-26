from typing import Dict

from sqlalchemy import Column, Integer, String

from database import Base


class Company(Base):
    __tablename__ = "company"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(100), nullable=False)

    def __init__(self, name: str):
        self.name = name


class Transform:
    @staticmethod
    def from_mock_to_company(data: Dict) -> Company:
        return Company(id=data['identification'], name=data['company_description'])

    def from_company_to_mock(company: Company) -> Dict:
        return {"identification": company.id, "company_description": company.name}