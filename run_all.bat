@echo off
set BASEDIR=%~dp0
start "Dashboard_Gateway" cmd /k "cd %BASEDIR%services\dashboard_gateway && C:\Content\APPS\Anaconda\python.exe -m uvicorn app.main:app --reload --log-config logging.yaml --port 8000"
timeout /t 1
start "Data_Service" cmd /k "cd %BASEDIR%services\data_service && C:\Content\APPS\Anaconda\python.exe -m uvicorn app.main:app --reload --log-config logging.yaml --port 8001"
timeout /t 1
start "Portfolio_Service" cmd /k "cd %BASEDIR%services\portfolio_service && C:\Content\APPS\Anaconda\python.exe -m uvicorn app.main:app --reload --log-config logging.yaml --port 8002"
timeout /t 1
start "Execution_Service" cmd /k "cd %BASEDIR%services\execution_service && C:\Content\APPS\Anaconda\python.exe -m uvicorn app.main:app --reload --log-config logging.yaml --port 8003"
timeout /t 1
start "Intraday_Streaming_Service" cmd /k "cd %BASEDIR%services\intraday_streaming_service && C:\Content\APPS\Anaconda\python.exe -m uvicorn app.main:app --reload --port 8004"
timeout /t 1
start "IPO_Strategy_Service" cmd /k "cd %BASEDIR%services\ipo_strategy_service && C:\Content\APPS\Anaconda\python.exe -m uvicorn app.main:app --reload --log-config logging.yaml --port 8010"
timeout /t 1
start "Daily_OHLCV_Service" cmd /k "cd %BASEDIR%services\daily_ohlcv_service && C:\Content\APPS\Anaconda\python.exe -m app.main"
timeout /t 1
start "Dashboard" cmd /k "cd %BASEDIR%services\my-dashboard && npm run dev"
