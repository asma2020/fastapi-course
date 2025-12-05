from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# ───── THIS IS THE ONLY THING THAT MATTERS ON RAILWAY ─────
DATABASE_URL = os.getenv("DATABASE_URL")  # Railway injects this

# Fix postgres:// → postgresql:// (Railway uses postgres://)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# ───── ONLY FOR LOCAL DEVELOPMENT (when no DATABASE_URL) ─────
if not DATABASE_URL:
    from .config import settings
    DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# ───── Create engine with the correct URL ─────
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
