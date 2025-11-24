from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from fastapi import Depends
from .config import settings


# SQLALCHEMY_DATABASE_URL = 'postgresql://<usename>:<password>@<ip-address/hostname>/<database_name'
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql.app.db'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:123456@localhost/fastapi'
# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_name}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
## WRONG (you wrote this)
# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_name}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# CORRECT (copy-paste this exact line)
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# SQLALCHEMY_DATABASE_URL = 'postgresql://<usename>:<password>@<ip-address/hostname>/<database_name'
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql.app.db'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:123456@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)# if splite3 add connect_args={"check_same_thread":False} 

SessionLocal = sessionmaker(bind=engine, autocommit= False,autoflush= False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()