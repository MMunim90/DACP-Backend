from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from models import Users, Contests, Challenges, Platform_Stat
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from router.auth import get_current_user
from datetime import timedelta, datetime, timezone
from utils.contest_utils import calculate_contest_status

router = APIRouter()
class ContestsCreate(BaseModel):
    title: str
    writers: str
    category: str
    description: str = Field(default = '', max_length=300)
    length: float = Field(default=0.0, ge=0)
    start_at: datetime
    end_at: datetime
    
class ContestsUpdate(BaseModel):
    title: Optional[str] = Field(default=None)
    writers: Optional[str] = Field(default=None)
    category: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    length: Optional[float] = Field(default=None, ge=0)
    cover_image: Optional[str] = Field(default=None)
    start_at: Optional[datetime] = Field(default=None)
    end_at: Optional[datetime] = Field(default=None)

class UpdateUserRole(BaseModel):
    role : str
        
class UpdateUserStatus(BaseModel):
    is_active : bool
    
class PlatformStatUpdate(BaseModel):
    total_problems: Optional[int] = Field(default=None, ge=0)
    developers: Optional[int] = Field(default=None, ge=0)
    contests: Optional[int] = Field(default=None, ge=0)
    submissions: Optional[int] = Field(default=None, ge=0)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
    
    
@router.get('/admin/users/all')
def get_all_users(user: user_dependency, db: db_dependency):
    
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Failed Authentication')
    
    users = db.query(Users).all()
    return users


@router.put('/admin/update_user_role')
def update_user(user : user_dependency, db : db_dependency, user_id: int, update_user_role : UpdateUserRole):

    if user is None or user.get('role') != 'admin':
            raise HTTPException(status_code=401, detail='Failed Authentication')

    user = db.query(Users).filter(Users.id == user_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    update_role = update_user_role.model_dump(exclude_unset=True)

    user.role = update_user_role.role

    db.commit()
    return JSONResponse(status_code=200, content={'message' : 'User role updated successfully'})


@router.put('/admin/update_user_status')
def update_user(user : user_dependency, db : db_dependency, user_id: int, update_user_status : UpdateUserStatus):

    if user is None or user.get('role') != 'admin':
            raise HTTPException(status_code=401, detail='Failed Authentication')

    user = db.query(Users).filter(Users.id == user_id).first()
    
    if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

    update_status = update_user_status.model_dump(exclude_unset=True)

    user.is_active = update_user_status.is_active

    db.commit()
    return JSONResponse(status_code=200, content={'message' : 'User status updated successfully'})


@router.delete('/admin/remove_user/{user_id}')
def remove_user(user: user_dependency, db: db_dependency, user_id: int):
    
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Failed Authentication')
    
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found!')
    
    db.query(Users).filter(Users.id == user_id).delete()
        
    db.commit()
    
    return JSONResponse(status_code=200, content={'message': 'User removed successfully!'})


@router.post('/admin/create_contest')
def create_contest(
    user: user_dependency,
    db: db_dependency,
    new_contest: ContestsCreate
):

    if user is None or user.get('role') != 'admin':
        raise HTTPException(
            status_code=401,
            detail='Failed Authentication'
        )

    if new_contest.end_at <= new_contest.start_at:
        raise HTTPException(
            status_code=400,
            detail='Contest end time must be after start time'
        )

    contest_data = new_contest.model_dump(exclude={'status'})

    contest_model = Contests(**contest_data)

    contest_model.status = calculate_contest_status(contest_model)

    db.add(contest_model)
    db.commit()
    db.refresh(contest_model)

    return JSONResponse(
        status_code=201,
        content={'message': 'Contest added successfully'}
    )


@router.put('/admin/update_contest/{contest_id}')
def update_contest(
    user: user_dependency,
    db: db_dependency,
    update_contest: ContestsUpdate,
    contest_id: int
):

    if user is None or user.get('role') != 'admin':
        raise HTTPException(
            status_code=401,
            detail='Failed Authentication'
        )

    contest = db.query(Contests).filter(
        Contests.id == contest_id
    ).first()

    if contest is None:
        raise HTTPException(
            status_code=404,
            detail='Contest not found!'
        )

    update_data = update_contest.model_dump(
        exclude_unset=True,
        exclude={'status'}
    )

    new_start_at = update_data.get('start_at', contest.start_at)
    new_end_at = update_data.get('end_at', contest.end_at)

    if new_end_at <= new_start_at:
        raise HTTPException(
            status_code=400,
            detail='Contest end time must be after start time'
        )

    for key, value in update_data.items():
        setattr(contest, key, value)

    contest.status = calculate_contest_status(contest)

    db.commit()
    db.refresh(contest)

    return JSONResponse(
        status_code=200,
        content={
            'message': 'Contest updated successfully!'
        }
    )


@router.delete('/admin/delete_contest/{contest_id}')
def delete_contest(
    user: user_dependency,
    db: db_dependency,
    contest_id: int
):

    if user is None or user.get('role') != 'admin':
        raise HTTPException(
            status_code=401,
            detail='Failed Authentication'
        )

    contest = db.query(Contests).filter(
        Contests.id == contest_id
    ).first()

    if contest is None:
        raise HTTPException(
            status_code=404,
            detail='Contest not found!'
        )

    db.delete(contest)

    db.commit()

    return JSONResponse(
        status_code=200,
        content={
            'message': 'Contest deleted successfully!'
        }
    )
    
    
@router.put('/admin/update_platform_stat')
def update_platform_stat(
    user: user_dependency,
    db: db_dependency,
    update_platform_stat: PlatformStatUpdate):
    
    if user is None or user.get('role') != 'admin':
            raise HTTPException(
                status_code=401,
                detail='Failed Authentication'
            )
    
    platform_stat = db.query(Platform_Stat).first()
    
    if platform_stat is None:
        raise HTTPException(
            status_code=404,
            detail='Platform statistics not found.'
        )
    
    update_data = update_platform_stat.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(platform_stat, key, value)
    
    
    db.commit()
    db.refresh(platform_stat)
    
    return JSONResponse(
        status_code=200,
        content={
            'message': 'Platform Statistics updated successfully!'
        }
    )

