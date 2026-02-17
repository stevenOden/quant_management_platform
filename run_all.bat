@echo off
set BASEDIR=%~dp0
start "Data_Service" cmd /k "cd %BASEDIR%services\data_service && python -m uvicorn app.main:app --reload --port 8001"
start "Portfolio_Service" cmd /k "cd %BASEDIR%services\portfolio_service && python -m uvicorn app.main:app --reload --port 8002"
start "Execution_Service" cmd /k "cd %BASEDIR%services\execution_service && python -m uvicorn app.main:app --reload --port 8003"
start "Intraday_Streaming_Service" cmd /k "cd %BASEDIR%services\intraday_streaming_service && python -m uvicorn app.main:app --reload --port 8004"
::start "Daily_OHLCV_Service" cmd /k "cd %BASEDIR%services\daily_ohlcv_service && python -m app.main"
start "IPO_Strategy_Service" cmd /k "cd %BASEDIR%services\ipo_strategy_service && python -m uvicorn app.main:app --reload --port 8010"