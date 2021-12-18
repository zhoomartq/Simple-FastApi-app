from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm.session import Session
from schemas import Blog, ShowBlog
import models
from database import engine, SessionLocal
from passlib.context import CryptContext
from schemas import User
from oath2 import get_current_user


models.Base.metadata.create_all(engine) 


router = APIRouter(
    prefix = '/blog',
    tags = ['blog']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get('', response_model=List[ShowBlog])
def all(db : Session =  Depends(get_db), current_user: User = Depends(get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post('', status_code=status.HTTP_201_CREATED,)
def create(request: Blog, db : Session =  Depends(get_db), current_user: User = Depends(get_current_user)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db : Session =  Depends(get_db), current_user: User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with this id {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

@router.put('/{id}',  status_code=status.HTTP_202_ACCEPTED)
def update(id, request: Blog, db : Session =  Depends(get_db), current_user: User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with this id {id} not found')
    blog.update(request.dict())
    db.commit()
    return 'updated'





@router.get('/{id}',  status_code=status.HTTP_200_OK, response_model=ShowBlog)
def show(id, response: Response, db : Session =  Depends(get_db), current_user: User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f"blog with the id {id} is not available"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with the id {id} is not available")
    return blog
 

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
