from sqlalchemy import Column, Integer, String, DateTime,Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional,Any


Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"  

    user_ID = Column(Integer, primary_key=True, index=True,autoincrement=True)
    mail = Column(String(255), index=True, unique=True, nullable=False) 
    company_ID = Column(Integer, nullable=False)
    division_ID = Column(Integer, nullable=False)
    status_ID = Column(Integer, nullable=False)
    fechadecreacion = Column(DateTime, default=datetime.utcnow)
    create_by = Column(Integer, nullable=False)
    is_segura_user = Column(Boolean(10), nullable=False)


class User(BaseModel):
    user_ID: Optional[int] = None 
    mail: EmailStr
    company_ID: int
    division_ID: int
    status_ID: int
    fechadecreacion: Optional[datetime] = None  
    create_by: int
    is_segura_user: bool

    class Config:
        orm_mode = True
        from_attributes = True 

class UserResponse(BaseModel):
    status: str
    message: str
    data:  Optional[Any] = None 