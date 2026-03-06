import os
from dotenv import load_dotenv
from models import user_model
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.orm import sessionmaker

load_dotenv()

engine = create_engine(os.getenv("DATABASE_PUBLIC_URL"))


def get_session():
    with Session(engine) as session:
        yield session
