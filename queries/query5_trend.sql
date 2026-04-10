-- Daily Rugpull vs Healthy Launch Rate Trend
WITH daily_tokens AS (
  SELECT 
    DATE_TRUNC('day', created_time) as launch_date,
    COUNT(*) as total_tokens,
    COUNT(CASE 
      WHEN max_mcap > 20000 
        AND max_mcap_10m > 0.8 * max_mcap 
        AND mcap_1h < 0.2 * max_mcap 
      THEN 1 
    END) as rug_tokens,
    COUNT(CASE 
      WHEN max_mcap > 20000 
        AND mcap_1h > 0.8 * mcap_10m 
        AND mcap_4h > 0.2 * max_mcap 
      THEN 1 
    END) as healthy_tokens
  FROM dune.bumaye17.result_clean_pump_fun
  WHERE created_time >= NOW() - INTERVAL '30' DAY
  GROUP BY 1
)
SELECT 
  launch_date,
  total_tokens,
  rug_tokens,
  healthy_tokens,
  ROUND(rug_tokens * 100.0 / NULLIF(total_tokens, 0), 2) as rug_rate_pct,
  ROUND(healthy_tokens * 100.0 / NULLIF(total_tokens, 0), 2) as healthy_rate_pct
FROM daily_tokens
ORDER BY launch_date DESC
