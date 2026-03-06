import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { CONFIG } from '../config';

export function useDailyPnl() {
  return useQuery({
    queryKey: ['daily-pnl'],
    queryFn: async () => {
        const res = await axios.get(CONFIG.PORTFOLIO_DAILY_PNL_URL);
        return res.data;
    },
    refetchInterval: 5 * 60 * 1000, // 5 minutes
    staleTime: 5 * 60 * 1000, // treat data as fresh for 5 minutes
  });
}
