import { useDailyPnl } from '../hooks/useDailyPnl';
import DailyPnlChart from './DailyPnlChart';

export default function DailyPnlPanel() {
  const { data, isLoading } = useDailyPnl();

  if (isLoading) return <p>Loading daily PnL…</p>;

  return (
    <div>
      <h2>Daily Portfolio Value (1 Year)</h2>
      <DailyPnlChart data={data} />
    </div>
  );
}
