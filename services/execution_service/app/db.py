from sqlmodel import SQLModel, Session, create_engine
from app.models.trade import SystemState

DATABASE_URL = "sqlite:///./execution.db"
engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    # Ensure SystemState singleton row exists for synchronicity with portfolio
    with Session(engine) as session:
        state = session.get(SystemState, 1)
        if state is None:
            state = SystemState(id=1, portfolio_sync_required=False)
            session.add(state)
            session.commit()

def get_session():
    with Session(engine) as session:
        yield session