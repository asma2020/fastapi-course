from fastapi import FastAPI, Response, HTTPException,status,Depends,APIRouter
from typing import Optional, List
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import uvicorn
import time
from  app import models
from app.database import engine
from app.database import get_db
from sqlalchemy.orm import Session
from app import schemas 
from  app.schemas import PostBase as Post
from  app  import utils
# from .. import models,schemas,utils
models.Base.metadata.create_all(bind = engine)

app = FastAPI()
router = APIRouter(prefix='/users', tags=['Users'])
@router.post('/', status_code= status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db: Session = Depends(get_db)):      
#    new_post = models.Post(title = post.title, content = post.content,published = post.published)  
   hashed_password = utils.hash(user.password)
   user.password = hashed_password
   new_user = models.User(**user.dict())   
   db.add(new_user)
   db.commit()
   db.refresh(new_user)
   return new_user
@router.get('/{id}', response_model= schemas.UserOut)
def get_user(id:int, db:Session=Depends(get_db)):
    user= db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"user with id {id} not exist!")
    return user
