from fastapi import FastAPI, Response, HTTPException,status,Depends
from typing import Optional, List
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import uvicorn
import time
from app import models
from .database import engine
from .database import get_db
from sqlalchemy.orm import Session
from . import schemas 
from  .schemas import PostBase as Post
from . import utils

models.Base.metadata.create_all(bind = engine)

app = FastAPI()


@app.get('/sqlalchemy')
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status": posts }

@app.get('/posts', response_model= List[schemas.PostResponse])
def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return  posts

@app.post('/posts', status_code= status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_post(post:schemas.PostCreat,db: Session = Depends(get_db)):      
#    new_post = models.Post(title = post.title, content = post.content,published = post.published)  
   new_post = models.Post(**post.dict())
   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   return new_post

@app.get('/posts/{id}', response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found.")
    return post

@app.delete('/posts/{id}', response_model= schemas.BaseModel)
def delete_post(id: int, db: Session= Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f" post with id {id} didnt exist!")
    deleted_post.delete(synchronize_session= False)
    db.commit()
    return deleted_post
@app.put('/posts/{id}', response_model= schemas.PostResponse)
def update_posts(id:int,updated_post:Post, db:Session=Depends(get_db)):
    post_qury = db.query(models.Post).filter(models.Post.id == id)
    post = post_qury.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"id {id} does not exist")
    # post_qury.update({'title': 'update', 'content': 'whatever'},synchronize_session=False)
    post_qury.update(updated_post.dict(), synchronize_session = False)
    db.commit()
    return {"status": post_qury.first()}

@app.post('/users', status_code= status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db: Session = Depends(get_db)):      
#    new_post = models.Post(title = post.title, content = post.content,published = post.published)  
   hashed_password = utils.hash(user.password)
   user.password = hashed_password
   new_user = models.User(**user.dict())   
   db.add(new_user)
   db.commit()
   db.refresh(new_user)
   return new_user
@app.get('/users/{id}', response_model= schemas.UserOut)
def get_user(id:int, db:Session=Depends(get_db)):
    user= db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"user with id {id} not exist!")
    return user
if __name__ == "__main__":
    uvicorn.run(app)