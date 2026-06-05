import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# ── Read DATABASE_URL from environment
#    - Local development  → SQLite  (created automatically)
#    - Render production  → PostgreSQL (set DATABASE_URL in Render dashboard)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bokhary_messages.db")

# Render sometimes provides "postgres://" — SQLAlchemy needs "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# ── Engine
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

# ── Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ── Base class for ORM models
Base = declarative_base()
