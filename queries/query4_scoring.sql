-- Token Risk Scoring Model
SELECT 
  account_mint,
  symbol,
  max_mcap,
  buy_sol_vol_10s,
  sell_vol_sol_1m,
  first_buy_vol_sol,
  mcap_1h,
  mcap_4h,
  (CASE WHEN buy_sol_vol_10s > 50 THEN 3 WHEN buy_sol_vol_10s > 30 THEN 2 WHEN buy_sol_vol_10s > 15 THEN 1 ELSE 0 END) +
  (CASE WHEN sell_vol_sol_1m > 30 THEN 3 WHEN sell_vol_sol_1m > 15 THEN 2 WHEN sell_vol_sol_1m > 5 THEN 1 ELSE 0 END) +
  (CASE WHEN first_buy_vol_sol > 20 THEN 2 WHEN first_buy_vol_sol > 10 THEN 1 ELSE 0 END) +
  (CASE WHEN mcap_1h < 0.2 * max_mcap THEN 2 ELSE 0 END) as risk_score,
  CASE 
    WHEN max_mcap_10m > 0.8 * max_mcap AND mcap_1h < 0.2 * max_mcap THEN 'CONFIRMED_RUG'
    WHEN mcap_1h > 0.8 * mcap_10m AND mcap_4h > 0.2 * max_mcap THEN 'CONFIRMED_HEALTHY'
    ELSE 'UNKNOWN'
  END as actual_label
FROM dune.bumaye17.result_clean_pump_fun
WHERE max_mcap > 20000
ORDER BY risk_score DESC
LIMIT 500
