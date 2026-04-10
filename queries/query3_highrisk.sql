-- Current High-Risk Tokens (Live Feed)
SELECT 
  account_mint,
  symbol,
  created_time,
  buy_sol_vol_10s,
  sell_vol_sol_1m,
  first_buy_vol_sol,
  mcap_first_buy,
  mcap_10m,
  mcap_1h,
  max_mcap,
  CASE 
    WHEN buy_sol_vol_10s > 50 AND sell_vol_sol_1m > 15 THEN '🔴 VERY HIGH RISK'
    WHEN buy_sol_vol_10s > 50 OR sell_vol_sol_1m > 15 THEN '🟡 HIGH RISK'
    WHEN buy_sol_vol_10s > 30 THEN '🟠 MODERATE RISK'
    ELSE '🟢 LOW RISK'
  END as risk_level
FROM dune.bumaye17.result_clean_pump_fun
WHERE max_mcap > 20000
  AND created_time >= NOW() - INTERVAL '7' DAY
  AND (buy_sol_vol_10s > 30 OR sell_vol_sol_1m > 10)
ORDER BY buy_sol_vol_10s DESC
LIMIT 100
