from sqlalchemy.orm import Session

from models import Company


class CompanyRepository:
    @staticmethod
    def find_all(db: Session) -> list[Company]:
        return db.query(Company).all()

    @staticmethod
    def save(db: Session, company: Company) -> Company:
        if company.id:
            db.merge(company)
        else:
            db.add(company)
        db.commit()
        return company

    @staticmethod
    def find_by_id(db: Session, id: int) -> Company:
        return db.query(Company).filter(Company.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(Company).filter(Company.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        company = db.query(Company).filter(Company.id == id).first()
        if company is not None:
            db.delete(company)
            db.commit()
