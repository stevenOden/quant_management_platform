import type { StrategyState }  from "../types/StrategyTypes";

export function DiscoveredTable({ title, rows }: { title: string; rows: StrategyState[] }) {
  return (
    <div style={{ border: "1px solid #e2e8f0", borderRadius: 8, padding: 8 }}>
      <h2 style={{ marginBottom: 12, fontSize: 18, fontWeight: 1200 }}>{title}</h2>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#242b30", textAlign: "center" ,borderBottom: "2px solid #030303",}}>
            <th style={{ padding: "8px 12px" }}>Symbol</th>
            <th style={{ padding: "8px 12px" }}>IPO_Date</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr
              key={row.symbol + idx}
              style={{
                background: idx % 2 === 0 ? "#20272b" : "#2c3e31",
                borderBottom: "2px solid #030303",
              }}>
              <td>{row.symbol}</td>
              <td>{row.ipo_date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function WatchingTable({ title, rows }: { title: string; rows: StrategyState[] }) {
  return (
    <div style={{ border: "1px solid #e2e8f0", borderRadius: 8, padding: 8 }}>
      <h2 style={{ marginBottom: 12, fontSize: 18, fontWeight: 1200 }}>{title}</h2>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#242b30", textAlign: "center" ,borderBottom: "2px solid #030303",}}>
            <th style={{ padding: "8px 12px" }}>Symbol</th>
            <th style={{ padding: "8px 12px" }}>IPO_Date</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr
              key={row.symbol + idx}
              style={{
                background: idx % 2 === 0 ? "#20272b" : "#2c3e31",
                borderBottom: "2px solid #030303",
              }}
            >
              <td style={{ padding: "8px 12px" }}>{row.symbol}</td>
              <td style={{ padding: "8px 12px" }}>{row.ipo_date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function IpoDayTable({ title, rows }: { title: string; rows: StrategyState[] }) {
  return (
    <div style={{ border: "1px solid #e2e8f0", borderRadius: 8, padding: 8 }}>
      <h2 style={{ marginBottom: 12, fontSize: 18, fontWeight: 1200 }}>{title}</h2>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#242b30", textAlign: "center" ,borderBottom: "2px solid #030303",}}>
            <th style={{ padding: "8px 12px" }}>Symbol</th>
            <th style={{ padding: "8px 12px" }}>IPO_Date</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr
              key={row.symbol + idx}
              style={{
                background: idx % 2 === 0 ? "#20272b" : "#2c3e31",
                borderBottom: "2px solid #030303",
              }}>
              <td>{row.symbol}</td>
              <td>{row.ipo_date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function ReadyTable({ title, rows }: { title: string; rows: StrategyState[] }) {
  return (
    <div style={{ border: "1px solid #e2e8f0", borderRadius: 8, padding: 8 }}>
      <h2 style={{ marginBottom: 12, fontSize: 18, fontWeight: 1200 }}>{title}</h2>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#242b30", textAlign: "center" ,borderBottom: "2px solid #030303",}}>
            <th style={{ padding: "8px 12px" }}>Symbol</th>
            <th style={{ padding: "8px 12px" }}>IPO_Date</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr
              key={row.symbol + idx}
              style={{
                background: idx % 2 === 0 ? "#20272b" : "#2c3e31",
                borderBottom: "2px solid #030303",
              }}>
              <td>{row.symbol}</td>
              <td>{row.ipo_date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function BuyTable({ title, rows }: { title: string; rows: StrategyState[] }) {
  return (
    <div style={{ border: "1px solid #e2e8f0", borderRadius: 8, padding: 8 }}>
      <h2 style={{ marginBottom: 12, fontSize: 18, fontWeight: 1200 }}>{title}</h2>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#242b30", textAlign: "center" ,borderBottom: "2px solid #030303",}}>
            <th style={{ padding: "8px 12px" }}>Symbol</th>
            <th style={{ padding: "8px 12px" }}>IPO_Date</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr
              key={row.symbol + idx}
              style={{
                background: idx % 2 === 0 ? "#20272b" : "#2c3e31",
                borderBottom: "2px solid #030303",
              }}>
              <td>{row.symbol}</td>
              <td>{row.ipo_date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function HoldingTable({ title, rows }: { title: string; rows: StrategyState[] }) {
  return (
    <div style={{ border: "1px solid #e2e8f0", borderRadius: 8, padding: 8 }}>
      <h2 style={{ marginBottom: 12, fontSize: 18, fontWeight: 1200 }}>{title}</h2>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#242b30", textAlign: "center" ,borderBottom: "2px solid #030303",}}>
            <th style={{ padding: "8px 12px" }}>Symbol</th>
            <th style={{ padding: "8px 12px" }}>PnL</th>
            <th style={{ padding: "8px 12px" }}>Price</th>
            <th style={{ padding: "8px 12px" }}>Target</th>
            <th style={{ padding: "8px 12px" }}>Stop</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr
              key={row.symbol + idx}
              style={{
                background: idx % 2 === 0 ? "#20272b" : "#2c3e31",
                borderBottom: "2px solid #030303",
              }}>
              <td>{row.symbol}</td>
              <td>{row.pnl_percent}</td>
              <td>{row.current_price}</td>
              <td>{row.target_price}</td>
              <td>{row.stop_loss}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function ExitedTable({ title, rows }: { title: string; rows: StrategyState[] }) {
  return (
    <div style={{ border: "1px solid #e2e8f0", borderRadius: 8, padding: 8 }}>
      <h2 style={{ marginBottom: 12, fontSize: 18, fontWeight: 1200 }}>{title}</h2>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#242b30", textAlign: "center" ,borderBottom: "2px solid #030303",}}>
            <th style={{ padding: "8px 12px" }}>Symbol</th>
            <th style={{ padding: "8px 12px" }}>PnL</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr
              key={row.symbol + idx}
              style={{
                background: idx % 2 === 0 ? "#20272b" : "#2c3e31",
                borderBottom: "2px solid #030303",
              }}>
              <td>{row.symbol}</td>
              <td>{row.pnl_percent}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}