export interface StrategyState {
  symbol: string;
  strategy: string;
  state: string;
  ipo_date: string;
  entry_price: number | null;
  entry_value: number | null;
  target_price: number | null;
  stop_loss: number | null;
  pnl: number | null;
  pnl_percent: number | null;
  last_evaluated: string | null;
  current_price: number | null;
}

export interface IPOStateResponse {
  DISCOVERED: StrategyState[];
  WATCHING: StrategyState[];
  IPO_DAY: StrategyState[];
  READY: StrategyState[];
  BUY_SIGNAL: StrategyState[];
  SELL_SIGNAL: StrategyState[];
  HOLDING: StrategyState[];
  EXITED: StrategyState[];
  MISSED: StrategyState[];
}
