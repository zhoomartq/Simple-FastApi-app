from typing import Optional, List
from fastapi import FastAPI
from pydantic import BaseModel


class Blog(BaseModel):
    id: int
    title: str
    body: str
    

    class Config: 
        orm_mode = True



class User(BaseModel): 
    name: str
    email: str
    password: str

    class Config: 
        orm_mode = True


class ShowUser(BaseModel): 
    id: int
    name: str
    email: str
    blog: List[Blog] = []

    class Config: 
        orm_mode = True


class ShowBlog(BaseModel):
    id: int
    title: str
    body: str
    creator: User

    class Config: 
        orm_mode = True