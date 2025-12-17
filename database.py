
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "sqlite:///chat.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Creates the tables if they don't exist."""
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")

def get_db():
    """Returns a new database session."""
    return SessionLocal()