from sqlmodel import SQLModel, create_engine, Session
## DEBUG
# DATABASE_URL = "sqlite:///./app/ipo_strategy.db"
DATABASE_URL = "sqlite:///./ipo_strategy.db" # <- Use this when done dubugging
## END DEBUG
engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def async_session():
    with Session(engine) as session:
        yield session