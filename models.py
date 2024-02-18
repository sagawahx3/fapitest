from sqlalchemy import Column, Integer, String

from database import Base


class Company(Base):
    __tablename__ = "company"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(100), nullable=False)
