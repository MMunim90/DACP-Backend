from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from datetime import datetime


class Users(Base):
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique = True)
    username = Column(String, unique = True)
    firstname = Column(String)
    lastname = Column(String)
    hash_password = Column(String)
    rating = Column(Integer, default = 0)
    is_active = Column(Boolean, default = True)
    role = Column(String) # admin or developer
    phone_number = Column(String)
    created_at = Column(DateTime, default = datetime.now())
    
    
class Contests(Base):
    
    __tablename__ = 'contests'
    
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable=False)
    writers = Column(String, nullable=True)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String(20), default = "upcoming", nullable=False) # upcoming or running or past
    length = Column(Float, default=0.0, nullable=False)
    cover_image = Column(String, nullable=True)
    created_at = Column(DateTime, default = datetime.now())
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)
    
    
class Challenges(Base):
    
    __tablename__ = 'challenges'
    
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable=False)
    writers = Column(String, nullable=True)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    difficulty = Column(String(20), nullable=False, default="beginner") # beginner or intermediate or advance 
    created_at = Column(DateTime, default = datetime.now())
