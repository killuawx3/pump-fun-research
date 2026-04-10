-- Top Serial Rugpull Creators
WITH creator_stats AS (
  SELECT 
    created_user as creator,
    COUNT(*) as total_tokens,
    COUNT(CASE 
      WHEN max_mcap > 20000 
        AND max_mcap_10m > 0.8 * max_mcap 
        AND mcap_1h < 0.2 * max_mcap 
      THEN 1 
    END) as rug_count,
    COUNT(CASE WHEN max_mcap > 20000 THEN 1 END) as meaningful_tokens,
    SUM(max_mcap) as total_max_mcap,
    AVG(buy_sol_vol_10s) as avg_buy_spike
  FROM dune.bumaye17.result_clean_pump_fun
  GROUP BY 1
  HAVING COUNT(*) > 3
)
SELECT 
  creator,
  total_tokens,
  rug_count,
  meaningful_tokens,
  ROUND(rug_count * 100.0 / NULLIF(meaningful_tokens, 0), 2) as rug_rate_pct,
  ROUND(total_max_mcap, 0) as total_mcap,
  ROUND(avg_buy_spike, 2) as avg_buy_spike_10s
FROM creator_stats
WHERE rug_count > 0
ORDER BY rug_count DESC, total_tokens DESC
LIMIT 50
