from datetime import timedelta
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from JWTtoken import create_access_token
import schemas
from .blog import get_db
from models import User
from hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(
    prefix = '/login',
    tags = ['login']

)

@router.post('')
def login(request: OAuth2PasswordRequestForm =  Depends(), db : Session =  Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user is not defined')
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'incorrect')
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

