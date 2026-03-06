import { useIntradayPnl } from '../hooks/useIntradayPnl';
import IntradayPnlChart from './IntradayPnlChart';

export default function IntradayPnlPanel() {
  const { data, isLoading } = useIntradayPnl();

  if (isLoading) return <p>Loading Intraday PnL…</p>;

  return (
    <div>
      <h2>Intraday Portfolio Value (24 hours)</h2>
      <IntradayPnlChart data={data} />
    </div>
  );
}
