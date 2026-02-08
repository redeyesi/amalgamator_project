import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "amalgamator.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def get_session() -> Session:
    """Returns a new database session."""
    return SessionLocal()
