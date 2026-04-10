-- =============================================================================
-- Pump.fun Rugpull Detection Dashboard - Dune Queries
-- =============================================================================

-- Query 1: Token Launch Statistics (Overview)
-- Name: pump.fun Token Launch Overview
-- Description: Distribution of tokens by max market cap tiers
-- Visualization: Bar chart
-- =============================================================================
SELECT 
  CASE 
    WHEN max_mcap < 7000 THEN '1. Dead on Arrival (<$7K)'
    WHEN max_mcap < 20000 THEN '2. Low Traction ($7K-$20K)'
    WHEN max_mcap < 100000 THEN '3. Medium Traction ($20K-$100K)'
    WHEN max_mcap < 1000000 THEN '4. High Traction ($100K-$1M)'
    ELSE '5. Over $1M'
  END as tier,
  COUNT(*) as token_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM dune.bumaye17.result_clean_pump_fun
GROUP BY 1
ORDER BY 1;

-- =============================================================================
-- Query 2: Top Rugpull Risk Signals
-- Name: Rugpull Risk Signals Distribution
-- Description: Feature distributions for early detection
-- Visualization: Table with color coding
-- =============================================================================
WITH rug_tokens AS (
  SELECT *,
    'RUG' as label
  FROM dune.bumaye17.result_clean_pump_fun
  WHERE max_mcap > 20000
    AND max_mcap_10m > 0.8 * max_mcap  -- peaked in first 10min
    AND mcap_1h < 0.2 * max_mcap       -- crashed by 1hr
),
healthy_tokens AS (
  SELECT *,
    'HEALTHY' as label
  FROM dune.bumaye17.result_clean_pump_fun
  WHERE max_mcap > 20000
    AND mcap_1h > 0.8 * mcap_10m       -- still growing at 1hr
    AND mcap_4h > 0.2 * max_mcap       -- maintained value
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
ORDER BY 1 DESC;

-- =============================================================================
-- Query 3: High-Risk Token Live Feed
-- Name: Current High-Risk Tokens (Live)
-- Description: Tokens with suspicious volume patterns
-- Visualization: Table
-- =============================================================================
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
LIMIT 100;

-- =============================================================================
-- Query 4: Rugpull Pattern Detection Score
-- Name: Token Risk Scoring Model
-- Description: Automated risk score based on early signals
-- Visualization: Scatter plot (Risk Score vs Max Mcap)
-- =============================================================================
SELECT 
  account_mint,
  symbol,
  max_mcap,
  buy_sol_vol_10s,
  sell_vol_sol_1m,
  first_buy_vol_sol,
  mcap_1h,
  mcap_4h,
  -- Risk scoring
  (CASE WHEN buy_sol_vol_10s > 50 THEN 3 WHEN buy_sol_vol_10s > 30 THEN 2 WHEN buy_sol_vol_10s > 15 THEN 1 ELSE 0 END) +
  (CASE WHEN sell_vol_sol_1m > 30 THEN 3 WHEN sell_vol_sol_1m > 15 THEN 2 WHEN sell_vol_sol_1m > 5 THEN 1 ELSE 0 END) +
  (CASE WHEN first_buy_vol_sol > 20 THEN 2 WHEN first_buy_vol_sol > 10 THEN 1 ELSE 0 END) +
  (CASE WHEN mcap_1h < 0.2 * max_mcap THEN 2 ELSE 0 END) as risk_score,
  -- Actual outcome
  CASE 
    WHEN max_mcap_10m > 0.8 * max_mcap AND mcap_1h < 0.2 * max_mcap THEN 'CONFIRMED_RUG'
    WHEN mcap_1h > 0.8 * mcap_10m AND mcap_4h > 0.2 * max_mcap THEN 'CONFIRMED_HEALTHY'
    ELSE 'UNKNOWN'
  END as actual_label
FROM dune.bumaye17.result_clean_pump_fun
WHERE max_mcap > 20000
ORDER BY risk_score DESC
LIMIT 500;

-- =============================================================================
-- Query 5: Daily Rugpull Rate Trend
-- Name: Daily Rugpull vs Healthy Launch Rate
-- Description: Time series of rugpull patterns over time
-- Visualization: Line chart
-- =============================================================================
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
ORDER BY launch_date DESC;

-- =============================================================================
-- Query 6: Top Serial Rugpull Creators
-- Name: Creator Reputation Tracker
-- Description: Wallets with multiple rug patterns
-- Visualization: Table
-- =============================================================================
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
  HAVING COUNT(*) > 3  -- at least 3 tokens launched
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
LIMIT 50;
