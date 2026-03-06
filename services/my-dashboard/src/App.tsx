import { PortfolioOverviewPanel } from './components/PortfolioOverviewPanel';
import DailyPnlPanel from './components/DailyPnlPanel';
import IntradayPnlPanel from './components/IntradayPnlPanel';
import { IpoStrategyStatesPanel } from './components/IpoStrategyStatePanel';
import './App.css'

function App() {
  return (
    //<div style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <div style={{ display: "grid", gridTemplateRows: "auto auto auto", gap: "30px", padding: "1px"}}>
      <PortfolioOverviewPanel />
        <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "20px",
        }}

      >
        <DailyPnlPanel />
        <IntradayPnlPanel />
      </div>

      <IpoStrategyStatesPanel />
      
    </div>
  );
}

export default App
