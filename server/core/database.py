import os
from dotenv import load_dotenv
from models import user_model
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5433")
DATABASE_NAME = os.getenv("DATABASE_NAME", "casebot")

pg_url = f"postgresql://postgres:Bilal%409002@localhost:5433/casebot"

engine = create_engine(pg_url)


def get_session():
    with Session(engine) as session:
        yield session
