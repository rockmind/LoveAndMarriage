from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, String, ARRAY
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class UserDBModel(Base):
    __tablename__ = "users"

    user_name = Column(String, primary_key=True, unique=True)
    hashed_password = Column(String, nullable=False)
    apps = Column(ARRAY(String), nullable=False)
    active = Column(Boolean, nullable=False)
    email = Column(String)
    full_name = Column(String)
    descriptions = Column(String)


class User(BaseModel):
    user_name: str
    hashed_password: str
    active: bool
    apps: List[str]
    email: Optional[str] = None
    full_name: Optional[str] = None
    descriptions: Optional[str] = None

    class Config:
        orm_mode = True
