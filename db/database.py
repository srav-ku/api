import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration
# DATABASE_URL = os.getenv("DATABASE_URL")
# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL environment variable is required")

def get_database_url():
    """
    Retrieves the database URL from environment variables.
    Prioritizes DATABASE_URL, falls back to SQLite for local development if needed.
    """
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return db_url
    else:
        # Use SQLite for local development if DATABASE_URL is not set
        print("Warning: DATABASE_URL not set. Using SQLite for local development.")
        return "sqlite:///./movie_api.db"


# Create SQLAlchemy engine
DATABASE_URL = get_database_url()
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

def get_database():
    """Get database session dependency for FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """Drop all database tables."""
    Base.metadata.drop_all(bind=engine)