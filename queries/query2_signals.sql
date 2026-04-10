-- Rugpull Risk Signals Distribution
WITH rug_tokens AS (
  SELECT *,
    'RUG' as label
  FROM dune.bumaye17.result_clean_pump_fun
  WHERE max_mcap > 20000
    AND max_mcap_10m > 0.8 * max_mcap
    AND mcap_1h < 0.2 * max_mcap
),
healthy_tokens AS (
  SELECT *,
    'HEALTHY' as label
  FROM dune.bumaye17.result_clean_pump_fun
  WHERE max_mcap > 20000
    AND mcap_1h > 0.8 * mcap_10m
    AND mcap_4h > 0.2 * max_mcap
)
SELECT 
  label,
  COUNT(*) as token_count,
  ROUND(AVG(buy_sol_vol_10s), 2) as avg_buy_vol_10s,
  ROUND(APPROX_PERCENTILE(buy_sol_vol_10s, 0.5), 2) as median_buy_vol_10s,
  ROUND(AVG(sell_vol_sol_1m), 2) as avg_sell_vol_1m,
  ROUND(APPROX_PERCENTILE(sell_vol_sol_1m, 0.5), 2) as median_sell_vol_1m,
  ROUND(AVG(first_buy_vol_sol), 2) as avg_first_buy,
  ROUND(APPROX_PERCENTILE(first_buy_cnt, 0.5), 0) as median_first_buy_cnt
FROM (
  SELECT * FROM rug_tokens
  UNION ALL
  SELECT * FROM healthy_tokens
)
GROUP BY 1
ORDER BY 1 DESC
