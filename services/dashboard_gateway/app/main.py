from fastapi import FastAPI, APIRouter
from app.routes import portfolio, trade_history, ipo_strategy, websocket
import yaml
from pathlib import Path
import logging.config

class HealthFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # Block only /health requests
        return "/health" not in record.getMessage()

config_path = Path(__file__).parent / ".." / "logging.yaml"
with config_path.open("r") as fin:
    config = yaml.safe_load(fin)
    logging.config.dictConfig(config)

# Attach filter to uvicorn access logger
logging.getLogger("uvicorn.access").addFilter(HealthFilter())

api_router = APIRouter()

api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
api_router.include_router(trade_history.router, prefix="/trades", tags=["trades"])
api_router.include_router(ipo_strategy.router, prefix="/ipo_strategy", tags=["strategy"])
api_router.include_router(websocket.router, tags=["websocket"])
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Dashboard Gateway")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(api_router)

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="debug",
    )