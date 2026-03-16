import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts';

type IntradayPnlPoint = {
  timestamp: string;
  portfolio_value: number;
};

type IntradayPnlChartProps = {
  data: IntradayPnlPoint[];
};

export default function IntradayPnlChart({ data }: IntradayPnlChartProps) {
    // data is an array of objects with date + total_pnl
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="timestamp" />
        <YAxis />
        <Tooltip />
        <Line
          type="monotone"
          dataKey="portfolio_value"
          stroke="#4f46e5"
          strokeWidth={2}
          dot={false}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

