import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


# Load environment variables
load_dotenv()


# PostgreSQL connection URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured. "
        "Please add it to the .env file."
    )


# SQLAlchemy base class
class Base(DeclarativeBase):
    pass


# PostgreSQL engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# Database session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db():
    """Provide a database session for FastAPI requests."""

    db: Session = SessionLocal()

    try:
        yield db
    finally:
        db.close()