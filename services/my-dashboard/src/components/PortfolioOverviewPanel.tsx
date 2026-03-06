import { usePortfolioOverview } from '../hooks/usePortfolioOverview';

export function PortfolioOverviewPanel() {
  const { data, isLoading, isError } = usePortfolioOverview();

  if (isLoading) {
    return <div>Loading portfolio overview…</div>;
  }

  if (isError) {
    return <div>Error loading portfolio overview</div>;
  }

  return (
    <div       style={{
        display: "grid",
        gridTemplateRows: "auto auto",
        gap: "10px",
        padding: "8px",
        border: "1px solid #ddd",
        borderRadius: "8px",
      }}
      >
      {/* Row 1: Title */}
      <h2 style={{ margin: 0 }}>Portfolio Overview</h2>

      {/* Row 2: Metrics in a single horizontal line */}
      <div
        style={{
          display: "flex",
          gap: "20px",
          alignItems: "center",
        }}
      >

      <p><strong>Total Value:</strong> {data.total_value}</p>
      <p><strong>Total PnL:</strong> {data.current_pnl}{' '}
      <span style={{ color: data.pnl_percent>= 0 ? 'green' : 'red' }}>
        ({data.pnl_percent > 0? '+${data.pnl_percent}' : data.pnl_percent}%)
      </span>
      </p>
      <p><strong>Unrealized PnL:</strong> {data.unrealized_pnl}{' '}
      <span style={{ color: data.unrealized_pnl_percent>= 0 ? 'green' : 'red' }}>
        ({data.unrealized_pnl_percent > 0? '+${data.unrealized_pnl_percent}' : data.unrealized_pnl_percent}%)
      </span>
      </p>
      <p><strong>Realized PnL:</strong> {data.realized_pnl}{' '}
      <span style={{ color: data.realized_pnl_percent>= 0 ? 'green' : 'red' }}>
        ({data.realized_pnl_percent > 0? '+${data.realized_pnl_percent}' : data.realized_pnl_percent}%)
      </span>
      </p>
      <p><strong>Buying Power:</strong> {data.cash}</p>
    </div>
    </div>
  );
}
