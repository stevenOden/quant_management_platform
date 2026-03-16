import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts';

type DailyPnlPoint = {
  timestamp: string;
  portfolio_value: number;
};

type DailyPnlChartProps = {
  data: DailyPnlPoint[];
};

export default function DailyPnlChart({ data }: DailyPnlChartProps) {
    // data is an array of objects with date + total_pnl
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="datestamp" />
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

