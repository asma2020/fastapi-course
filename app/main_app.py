from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from . import models
from .database import engine
from .routers import post, user, oauth,vote
# from .config import settings
# from pydantic import BaseSetting
# from pydantic_settings import BaseSettings

# pip freeze > requirement.txt

# class Setting(BaseSettings):
#     database_password: str = "localhost"
#     database_username: str = "postgres"
#     secret_key: str = "234ui234089234"

# setting = Setting()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(oauth.router)
app.include_router(vote.router)



@app.get("/")
def root():
    return {"message": "Hello World pushing out"}


if __name__ == "__main__":
    uvicorn.run(app)