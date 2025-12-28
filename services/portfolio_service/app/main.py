from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import create_db_and_tables
from app.routes.portfolio import router as portfolio_router
from app.routes.admin import router as admin_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown logic: close connections, flush buffers etc.

app = FastAPI(title="Portfolio Service",lifespan=lifespan)
app.include_router(portfolio_router)
app.include_router(admin_router)

