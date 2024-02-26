from typing import Union

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from database import engine, Base, get_db
from models import Company, Transform
from repository import CompanyRepository
from schemas import CompanyRequest, CompanyResponse
import httpx

Base.metadata.create_all(bind=engine)

# starting FastAPI
app = FastAPI()


@app.post("/company", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create(request: CompanyRequest, db: Session = Depends(get_db)):
    company = CompanyRepository.save(db, Company(**request.dict()))
    return CompanyResponse.from_orm(company)


@app.get("/company", response_model=list[CompanyResponse])
def find_all(db: Session = Depends(get_db)):
    companies = CompanyRepository.find_all(db)
    return [CompanyResponse.from_orm(company) for company in companies]


@app.get("/company/{id}", response_model=CompanyResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    company = CompanyRepository.find_by_id(db, id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found."
        )
    return CompanyResponse.from_orm(company)


@app.delete("/company/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    if not CompanyRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found."
        )
    CompanyRepository.delete_by_id(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/company/{id}", response_model=CompanyResponse)
def update(id: int, request: CompanyRequest, db: Session = Depends(get_db)):
    if not CompanyRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado"
        )
    company = CompanyRepository.save(db, Company(id=id, **request.dict()))
    return CompanyResponse.from_orm(company)


@app.get("/mock")
def return_mock():
    return {"identification": 2, "company_description": "Mock Name"}


@app.get("/mock/getcompany")
async def get_company():
    # no caso aqui seria a classe Store, certo?
    async with httpx.AsyncClient() as client:
        mock_response = await client.get("http://127.0.0.1:8000/mock")

        if mock_response.status_code == 200:
            json_data = mock_response.json()
        else:
            raise HTTPException(status_code=500, detail="Failed to fetch mock data")

    company_obj = Transform.from_mock_to_company(json_data)

    return company_obj


@app.post("/mock/createmock")
async def create_company(name: str):
    company_obj = Company(name=name)

    json_data = Transform.from_company_to_mock(company_obj)

    return json_data
