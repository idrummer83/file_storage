from sqlalchemy import Column, Integer, String

from .database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, unique=False, index=True)
    name = Column(String, unique=False, index=True)
    size = Column(Integer, index=True)
