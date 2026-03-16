from sqlmodel import SQLModel, create_engine, Session
import os

## DEBUG
# DATABASE_URL = "sqlite:///./app/ipo_strategy.db"
DATABASE_URL = "sqlite:///./ipo_strategy.db" # <- Use this when done dubugging
## END DEBUG

# Postgres connection; DATABASE_URL defined in docker-compose
DATABASE_URL = os.getenv("DATABASE_URL","sqlite:///./ipo_strategy.db")

engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# ## Asynchronous Engine
# async_engine = create_async_engine(DATABASE_URL, echo=False, future=True)
# AsyncSessionLocal = sessionmaker(async_engine,class_=AsyncSession,expire_on_commit=False)
#
# async def get_async_session() -> AsyncSession:
#     async with AsyncSessionLocal() as a_session:
#         yield a_session