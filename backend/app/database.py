import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

logger = logging.getLogger(__name__)

# Fallback mechanism to SQLite for local development convenience
db_url = settings.DATABASE_URL
engine_args = {}

if "postgresql" in db_url:
    try:
        # Check if database is accessible
        engine = create_engine(db_url, connect_args={"connect_timeout": 3})
        engine.connect()
        logger.info("Successfully connected to PostgreSQL")
    except Exception as e:
        logger.warning(f"PostgreSQL connection failed ({e}). Falling back to SQLite for local mode.")
        # Ensure data folder exists
        import os
        os.makedirs("./data", exist_ok=True)
        db_url = "sqlite:///./data/talentmind.db"
else:
    # SQLite configuration
    engine_args["connect_args"] = {"check_same_thread": False}

engine = create_engine(db_url, **engine_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
