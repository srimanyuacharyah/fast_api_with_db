from schemas.user_schemas import UserSchema
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from repositories.user_repo import UserRepo
from db import get_db
router = APIRouter()


@router.post("/signup")
def signup(user:UserSchema,db:Session=Depends(get_db)):
    user_repo=UserRepo(db)
    user_repo.add_user(user)
    return {"message": "User signed up successfully"}

@router.post("/login")
def login():
    return {"message": "User logged in successfully"}