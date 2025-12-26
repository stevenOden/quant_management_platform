For General information, platform overview and system architecture please see: 00_system_architecture/quant_mamangement_platform_architecture.pptx

market_data_fetcher: main.py lists the tickers to get data for
to run:
> cd C:\Content\Python_Projects\Github_Projects\quant_management_platform\services
> python -m market_data_fetcher.app.main

data_service: stores market data

> cd C:\Content\Python_Projects\Github_Projects\quant_management_platform\services\data_service
> python -m uvicorn app.main:app --reload --port 8001

portfolio_service: tracks open positions

> cd C:\Content\Python_Projects\Github_Projects\quant_management_platform\services\portfolio_service
> python -m uvicorn app.main:app --reload --port 8002

execution_service: executes trades

> cd C:\Content\Python_Projects\Github_Projects\quant_management_platform\services\execution_service
> python -m uvicorn app.main:app --reload --port 8003