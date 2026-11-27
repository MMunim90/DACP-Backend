from fastapi import FastAPI, Depends, HTTPException, Query, status
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, ConfigDict
import models
from models import Users, Contests, Challenges, Platform_Stat
from database import engine, SessionLocal
from fastapi.responses import JSONResponse
from router import admin, auth
from datetime import datetime
from router.auth import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from utils.contest_utils import calculate_contest_status
from sqlalchemy import or_

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        ""
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(admin.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class DeveloperPublicProfile(BaseModel):
    id: int
    firstname: Optional[str] = Field(default=None)
    lastname: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    email : Optional[str] = Field(default=None)
    profile_image: Optional[str] = Field(default=None)
    role: Optional[str] = Field(default=None)
    is_active: bool
    rating: int = 0
    max_rating: int = 0
    created_at: Optional[datetime] = Field(default=None)

    model_config = ConfigDict(from_attributes=True)


@app.get('/contests/all')
def get_all_contests(db: db_dependency):

    contests = db.query(Contests).all()

    updated = False

    for contest in contests:
        current_status = calculate_contest_status(contest)

        if contest.status != current_status:
            contest.status = current_status
            updated = True

    if updated:
        db.commit()

    return contests


@app.get('/contests/{contest_id}')
def get_single_contest(
    user: user_dependency,
    db: db_dependency,
    contest_id: int
):

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Failed Authentication"
        )

    contest = db.query(Contests).filter(
        Contests.id == contest_id
    ).first()

    if not contest:
        raise HTTPException(
            status_code=404,
            detail="Contest not found"
        )

    current_status = calculate_contest_status(contest)

    if contest.status != current_status:
        contest.status = current_status
        db.commit()
        db.refresh(contest)

    return contest


@app.get('/user_profile')
def get_user_profile(user : user_dependency, db : db_dependency):

    if user is None:
        raise HTTPException(status_code=401, detail="User did not logged in yet!!!")
    
    return db.query(Users).filter(Users.id == user.get('id')).first()


@app.get(
    "/developer_profile/{developer_id}",
    response_model=DeveloperPublicProfile
)
def get_developer_profile(
    developer_id: int,
    db: db_dependency
):
    developer = (
        db.query(Users)
        .filter(
            Users.id == developer_id,
            or_(
                Users.role == "developer",
                Users.role == "admin"
            )
        )
        .first()
    )

    if developer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Developer profile not found."
        )

    return developer


@app.get('/leaderboard')
def get_leaderboard(db: db_dependency):
    
    users = db.query(Users).all()
    return users


@app.get('/platform_stat')
def get_platform_stat(db: db_dependency):
    
    platform_stat = db.query(Platform_Stat).first()
    
    if platform_stat is None:
        raise HTTPException(
            status_code=404,
            detail='Platform statistics not found.'
        )
    
    return platform_stat