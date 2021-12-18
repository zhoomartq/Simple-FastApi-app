from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm.session import Session
from hashing import Hash
import models
from database import engine, SessionLocal
from passlib.context import CryptContext
import schemas



models.Base.metadata.create_all(engine) 


router = APIRouter(
    prefix= '/user',
    tags = ['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





@router.post('', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db : Session =  Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db : Session =  Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with the id {id} is not available")
    return user
