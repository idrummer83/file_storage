from sqlalchemy.orm import Session

from . import models


def get_file(db: Session, file_id: int):
    return db.query(models.File).filter(models.File.id == file_id).first()


def get_all_files(db: Session):
    return db.query(models.File).all()


def create_file(db: Session, file: dict):
    db_user = models.File(name=file.get('name'), size=file.get('size'))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
