from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import create_db_and_tables
from app.routes.execution import router as execution_router
from app.routes.admin import router as admin_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title= "Execution Service", lifespan=lifespan)
app.include_router(execution_router)
app.include_router(admin_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8003,
        reload=True,
        log_level="debug",
    )