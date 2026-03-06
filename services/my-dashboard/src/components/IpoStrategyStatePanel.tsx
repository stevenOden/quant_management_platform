import { useIpoStrategyStates } from '../hooks/useIpoStrategyStates';
import { DiscoveredTable,WatchingTable,IpoDayTable,ReadyTable,BuyTable,HoldingTable,ExitedTable } from './IpoStrategyStateTables';


export function IpoStrategyStatesPanel() {
  const { data, isLoading, isError } = useIpoStrategyStates();

  if (isLoading) {
    return <div>Loading IPO Strategy data…</div>;
  }

  if (isError) {
    return <div>Error loading IPO Strategy data</div>;
  }
  return(
    <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "20px" }}>
    <DiscoveredTable title="Discovered" rows={data.DISCOVERED} />
    <WatchingTable title="Watching" rows={data.WATCHING} />
    <IpoDayTable title="IPO Day" rows={data.IPO_DAY} />
    <ReadyTable title="Ready" rows={data.READY} />
    <BuyTable title="Buy Signal" rows={data.BUY_SIGNAL} />
    <HoldingTable title="Holding" rows={data.HOLDING} />
    <ExitedTable title="Exited" rows={data.EXITED} />
    </div>
  )

}

