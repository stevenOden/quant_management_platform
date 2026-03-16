from sqlmodel import SQLModel, create_engine, Session
import os

# Postgres connection; DATABASE_URL defined in docker-compose
DATABASE_URL = os.getenv("DATABASE_URL","sqlite:///./prices.db")

engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session