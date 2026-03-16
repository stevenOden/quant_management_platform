// const BASE_URL = import.meta.env.VITE_DASHBOARD_GATEWAY_SERVICE_URL ?? "http://localhost:8000"
const BASE_URL = "http://localhost:8000"

export const CONFIG = {
    PORTFOLIO_OVERVIEW_URL: `${BASE_URL}/portfolio/overview`,
    PORTFOLIO_DAILY_PNL_URL: `${BASE_URL}/portfolio/daily_pnl`,
    PORTFOLIO_INTRADAY_PNL_URL: `${BASE_URL}/portfolio/intraday_pnl`,
    STRATEGY_IPO_DATA_URL: `${BASE_URL}/ipo_strategy/ipo_events`,
}