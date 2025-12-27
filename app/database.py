from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL (change username, password, db name if needed)
DATABASE_URL = "postgresql://expense_qwbu_user:Ns2vlHqnrXQo1tnyCLhjExB8uF4gNefU@dpg-d56np72li9vc73fmmsc0-a.singapore-postgres.render.com/expense_qwbu"

# Create database engine
engine = create_engine(DATABASE_URL)

# SessionLocal = DB session used in routes
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all ORM models
Base = declarative_base()
