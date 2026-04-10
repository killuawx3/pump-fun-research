# Pump.fun Rugpull Detector - Dune Dashboard Setup

This guide will help you create a comprehensive Dune Analytics dashboard for detecting rugpull patterns on pump.fun.

## Dashboard Overview

**Name:** Pump.fun Rugpull Detector  
**Purpose:** Real-time detection of pump-and-dump schemes on pump.fun using on-chain signals  
**Data Source:** `dune.bumaye17.result_clean_pump_fun` (pre-computed token metrics)

---

## Classification Methodology

### RUG Token Definition
- Max market cap > $20,000
- **Peaked within 10 minutes:** `max_mcap_10m > 80% of max_mcap`
- **Crashed by 1 hour:** `mcap_1h < 20% of max_mcap`

### HEALTHY Token Definition
- Max market cap > $20,000
- **Still growing at 1 hour:** `mcap_1h > 80% of mcap_10m`
- **Maintained value at 4 hours:** `mcap_4h > 20% of max_mcap`

### Key Risk Signals
1. **Buy Volume in First 10 Seconds** - Median 34.41 SOL for rugs vs 5.09 SOL for healthy (6.8x difference)
2. **Sell Volume in First Minute** - Median 19.74 SOL for rugs vs 2.79 SOL for healthy (7.1x difference)
3. **First Buy Volume** - Large initial purchases indicate coordinated sniping

---

## Dashboard Setup Instructions

### Step 1: Create Queries on Dune

Go to [dune.com/queries](https://dune.com/queries) and create the following 6 queries:

#### Query 1: Token Launch Overview
**Name:** `Pump.fun Launch Statistics`  
**Description:** Distribution of tokens by market cap tier  
**File:** `queries/query1_overview.sql`

**Visualization Settings:**
- Type: **Bar Chart**
- X-axis: `tier`
- Y-axis: `token_count`
- Show percentage labels

---

#### Query 2: Rug vs Healthy Signal Comparison
**Name:** `Rugpull Risk Signals`  
**Description:** Compare volume patterns between rug and healthy tokens  
**File:** `queries/query2_signals.sql`

**Visualization Settings:**
- Type: **Table**
- Color coding:
  - `median_buy_vol_10s` > 30: Red
  - `median_sell_vol_1m` > 15: Red

---

#### Query 3: High-Risk Token Feed
**Name:** `Live High-Risk Tokens (7 Days)`  
**Description:** Recently launched tokens with suspicious patterns  
**File:** `queries/query3_highrisk.sql`

**Visualization Settings:**
- Type: **Table**
- Sort by: `buy_sol_vol_10s DESC`
- Conditional formatting on `risk_level` column

---

#### Query 4: Risk Scoring Model
**Name:** `Token Risk Score Analysis`  
**Description:** Automated risk scoring with validation  
**File:** `queries/query4_scoring.sql`

**Visualization Settings:**
- Type: **Scatter Plot**
- X-axis: `max_mcap` (log scale)
- Y-axis: `risk_score`
- Color by: `actual_label`
  - Red: CONFIRMED_RUG
  - Green: CONFIRMED_HEALTHY
  - Gray: UNKNOWN

---

#### Query 5: Daily Trend
**Name:** `Daily Rugpull Rate Trend`  
**Description:** Time series of rug patterns over 30 days  
**File:** `queries/query5_trend.sql`

**Visualization Settings:**
- Type: **Line Chart**
- X-axis: `launch_date`
- Y-axis: `rug_rate_pct` and `healthy_rate_pct`
- Two lines with different colors

---

#### Query 6: Creator Reputation
**Name:** `Serial Rugpull Creators`  
**Description:** Wallets with multiple rug patterns  
**File:** `queries/query6_creators.sql`

**Visualization Settings:**
- Type: **Table**
- Sort by: `rug_count DESC`
- Color coding:
  - `rug_rate_pct` > 60%: Red
  - `rug_rate_pct` 30-60%: Orange
  - `rug_rate_pct` < 30%: Yellow

---

### Step 2: Create Dashboard

1. Go to [dune.com/dashboards](https://dune.com/dashboards)
2. Click **"New Dashboard"**
3. Name it: **"Pump.fun Rugpull Detector"**
4. Add description:
   ```
   Real-time detection of pump-and-dump schemes on pump.fun using early volume signals.
   
   Methodology: Classifies tokens based on market cap trajectories in first 4 hours.
   RUG = peaked in 10min + crashed by 1hr.
   HEALTHY = growing at 1hr + maintained at 4hr.
   
   Key Signals: Buy volume spike in first 10 seconds (6.8x higher for rugs) 
   and sell volume in first minute (7.1x higher for rugs).
   ```

### Step 3: Add Queries to Dashboard

Add each query in this order:

#### Layout Recommendation:

**Row 1 (Full Width):**
- Query 1: Token Launch Overview (Bar Chart)

**Row 2 (50/50 Split):**
- Query 2: Rug vs Healthy Signals (Table)
- Query 5: Daily Trend (Line Chart)

**Row 3 (Full Width):**
- Query 3: High-Risk Token Feed (Table - scrollable)

**Row 4 (50/50 Split):**
- Query 4: Risk Score Scatter (Scatter Plot)
- Query 6: Serial Creators (Table)

### Step 4: Add Text Blocks

Add descriptive text blocks above each visualization:

**Above Query 3:**
```markdown
## 🚨 High-Risk Tokens (Last 7 Days)

Tokens flagged by the detector showing suspicious early volume patterns:
- 🔴 VERY HIGH RISK: buy_vol_10s > 50 SOL AND sell_vol_1m > 15 SOL
- 🟡 HIGH RISK: Either threshold exceeded
- 🟠 MODERATE RISK: buy_vol_10s > 30 SOL
```

**Above Query 6:**
```markdown
## 👤 Creator Reputation Tracker

Wallets with patterns of launching multiple rug tokens. High rug_rate_pct indicates serial bad actors.
```

---

## Dashboard URL

Once created, your dashboard will be at:
```
https://dune.com/your_username/pumpfun-rugpull-detector
```

Share this URL for public access or embed visualizations.

---

## Data Refresh

- Queries use the `dune.bumaye17.result_clean_pump_fun` table
- This is a **manually maintained community dataset** for January 5, 2025 data
- For live tracking, you would need to:
  1. Fork the data pipeline to compute these metrics real-time from `pumpdotfun_solana.pump_evt_tradeevent`
  2. Create a materialized view with incremental updates
  3. Use Dune's API to refresh on a schedule

---

## Customization Options

### Adjust Risk Thresholds
Modify the WHERE clauses in Query 3:
```sql
-- Current: Conservative (high confidence)
WHERE buy_sol_vol_10s > 30 OR sell_vol_sol_1m > 10

-- Alternative: Aggressive (catch more candidates)
WHERE buy_sol_vol_10s > 15 OR sell_vol_sol_1m > 5
```

### Add More Metrics
Extend Query 2 to include:
- `first_buy_cnt` (number of initial buyers)
- `mcap_retention_4h` (% of max mcap retained at 4hr)
- `sell_buy_ratio` (sell_vol / buy_vol in first hour)

### Creator History Depth
Modify Query 6 HAVING clause:
```sql
-- Current: At least 3 tokens
HAVING COUNT(*) > 3

-- For more established creators:
HAVING COUNT(*) > 10
```

---

## API Access (Optional)

To query these results programmatically:

```bash
# Using Dune CLI
dune query <query_id> --output results.csv

# Using Dune API
curl -X GET \
  "https://api.dune.com/api/v1/query/<query_id>/results" \
  -H "X-Dune-API-Key: YOUR_API_KEY"
```

---

## Notes & Limitations

1. **Historical Data Only:** The current dataset is from January 5, 2025. For real-time detection, you'd need to build a live pipeline.

2. **False Positives:** High buy volume in first 10 seconds can also indicate:
   - Legitimate hype/marketing
   - Celebrity/influencer endorsements
   - Lucky timing with viral content

3. **Classification Threshold:** The $20K minimum filters out 91% of tokens. Lower this to catch smaller rugs, but expect more noise.

4. **No Wallet Clustering:** This analysis doesn't track if snipers/dumpers are the same wallets across tokens. Adding wallet clustering would improve serial creator detection.

5. **Post-Graduation Tracking:** Tokens that graduate to PumpSwap/Raydium may still rug on the DEX. This detector only covers bonding curve phase.

---

## Next Steps

1. **Integrate Creator Wallet Graph:** Track funding sources and clustering
2. **Add Social Signals:** Twitter/Telegram activity correlation
3. **Build Alerting:** Telegram bot that pushes notifications when high-risk tokens are detected
4. **ML Model:** Train a classifier on the 208-token labeled dataset (163 rugs, 45 healthy)

---

## Contact

For questions or improvements, see the full research report at:
`/home/hermes/pump-fun-rugpull-detector/REPORT.md`
