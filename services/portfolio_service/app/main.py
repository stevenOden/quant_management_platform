import asyncio

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import create_db_and_tables
from app.routes.portfolio import router as portfolio_router
from app.routes.admin import router as admin_router
from app.routes.valuation import router as valuation_router
from app.services.valuation_orchestrator import valuation_loop

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    # Run background valuation loop that updates pnl snapshots for dashboard
    asyncio.create_task(valuation_loop())

    yield
    # Shutdown logic: close connections, flush buffers etc.

app = FastAPI(title="Portfolio Service",lifespan=lifespan)
app.include_router(portfolio_router)
app.include_router(admin_router)
app.include_router(valuation_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8002,
        reload=True,
        log_level="debug",
    )