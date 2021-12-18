from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm.session import Session
from schemas import Blog, ShowBlog
import models
from database import engine, SessionLocal
from passlib.context import CryptContext


models.Base.metadata.create_all(engine) 


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get('/blog', response_model=List[ShowBlog], tags=['blogs'])
def all(db : Session =  Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: Blog, db : Session =  Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog



@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def destroy(id, db : Session =  Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with this id {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

@router.put('/blog/{id}',  status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id, request: Blog, db : Session =  Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with this id {id} not found')
    blog.update(request.dict())
    db.commit()
    return 'updated'





@router.get('/blog/{id}',  status_code=status.HTTP_200_OK, response_model=ShowBlog, tags=['blogs'])
def show(id, response: Response, db : Session =  Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f"blog with the id {id} is not available"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with the id {id} is not available")
    return blog
 

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
