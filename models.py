from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, UniqueConstraint
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
    total_contest = Column(Integer, default = 0) # total contest participate
    total_problem = Column(Integer, default = 0) # total problem solved
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
    
    
class Contest_Registered(Base):
    
    __tablename__ = 'contest_registered'
        
    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    contest_id = Column(Integer, ForeignKey('contests.id'), nullable=False)
    ___table_args__ = (
        UniqueConstraint(
            "user_id",
            "contest_id",
            name="unique_user_contest_registration"
        ),
    )
    
class Challenges(Base):
    
    __tablename__ = 'challenges'
    
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable=False)
    writers = Column(String, nullable=True)
    description = Column(String, nullable=True)
    difficulty_rating = Column(Integer, nullable=False)
    difficulty = Column(String(20), nullable=False, default="beginner") # beginner or intermediate or advance 
    created_at = Column(DateTime, default = datetime.now)
    
    
class Submission(Base):
    
    __tablename__ = 'submission'
    
    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    challenges_id = Column(Integer, ForeignKey('challenges.id'))
    submitted_at = Column(DateTime, default = datetime.now)
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "challenges_id",
            name="unique_user_challenges_perception"
        ),
    )

class Platform_Stat(Base):
    
    __tablename__ = 'platform_stat'
    
    id = Column(Integer, primary_key=True, index=True)
    total_problems = Column(Integer, nullable=True)
    developers = Column(Integer, nullable=True)
    contests = Column(Integer, nullable=True)
    submissions = Column(Integer, nullable=True)

