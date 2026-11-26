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
    max_rating = Column(Integer, default = 0)
    is_active = Column(Boolean, default = True)
    role = Column(String) # admin or developer
    phone_number = Column(String)
    profile_image = Column(String, nullable=True)
    created_at = Column(DateTime, default = datetime.now)
    
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
    created_at = Column(DateTime, default = datetime.now)
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
    created_at = Column(DateTime, default = datetime.now)
    

class Books(Base):
    
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    author = Column(String)
    category = Column(String)
    description = Column(String)
    price = Column(Float, default=0.0)
    total_copies = Column(Integer, default=5)
    available_copies = Column(Integer, default=3)
    cover_image = Column(String, nullable=True)
    created_at = Column(DateTime, default = datetime.now())
    
    
    
class Reservations(Base):
    
    __tablename__ = 'reservations'
    
    id = Column(Integer, primary_key = True, index = True)
    book_id = Column(Integer, ForeignKey('books.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    reservation_date = Column(DateTime, default = datetime.now())
    status = Column(String, default = 'pending') # pending, approved, cancelled, rejected
    
    
class IssueRecords(Base):
    
    __tablename__ = 'issue_records'
    
    id = Column(Integer, primary_key = True, index = True)
    book_id = Column(Integer, ForeignKey('books.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    issue_date = Column(DateTime, default = datetime.now())
    due_date = Column(DateTime)
    return_date = Column(DateTime, nullable=True)
    status = Column(String, default = 'issued') # issued, returned, rejected
    fine_amount = Column(Float, default=0.0)
    fine_paid = Column(Boolean, default=False)