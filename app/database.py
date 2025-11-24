from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# ────────────────────────────────
# RAILWAY FIX — THIS IS THE KEY PART
# ────────────────────────────────
DATABASE_URL = os.getenv("DATABASE_URL")  # Railway gives this

# Railway uses "postgres://" but SQLAlchemy needs "postgresql://"
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# If running locally (no DATABASE_URL), fall back to your settings (for dev)
if not DATABASE_URL:
    from .config import settings
    DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# ────────────────────────────────
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
