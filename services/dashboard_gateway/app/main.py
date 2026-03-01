from fastapi import FastAPI, APIRouter
from app.routes import portfolio, trade_history, strategy, websocket

api_router = APIRouter()

api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
api_router.include_router(trade_history.router, prefix="/trades", tags=["trades"])
api_router.include_router(strategy.router, prefix="/strategy", tags=["strategy"])
api_router.include_router(websocket.router, tags=["websocket"])
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Dashboard Gateway")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="debug",
    )