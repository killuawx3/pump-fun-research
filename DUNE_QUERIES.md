# Dune Queries - Pump.fun Rugpull Detector

All queries have been created on Dune Analytics. Here are the direct links:

## Query Links

1. **Token Launch Overview** (ID: 6978007)
   - https://dune.com/queries/6978007
   - Bar chart showing token distribution by market cap tier

2. **High-Risk Token Feed** (ID: 6978008)
   - https://dune.com/queries/6978008
   - Live feed of suspicious launches in last 7 days

3. **Rugpull Risk Signals** (ID: 6978009)
   - https://dune.com/queries/6978009
   - Compare RUG vs HEALTHY volume patterns

4. **Token Risk Score Model** (ID: 6978010)
   - https://dune.com/queries/6978010
   - Automated risk scoring with validation

5. **Serial Rugpull Creators** (ID: 6978011)
   - https://dune.com/queries/6978011
   - Track wallets with multiple rug patterns

6. **Daily Rugpull Rate Trend** (ID: 6978012)
   - https://dune.com/queries/6978012
   - 30-day timeseries of rug rates

## Creating the Dashboard

### Quick Setup (5 minutes)

1. Go to: https://dune.com/dashboards/new
2. Name it: "Pump.fun Rugpull Detector"
3. Add description:
   ```
   Real-time detection of pump-and-dump schemes on pump.fun using on-chain volume signals.
   
   Key Signals:
   - Buy volume in first 10 seconds (6.8x higher for rugs)
   - Sell volume in first minute (7.1x higher for rugs)
   
   Methodology: Classifies tokens based on market cap trajectories.
   RUG = peaked in 10min + crashed by 1hr
   HEALTHY = growing at 1hr + maintained at 4hr
   ```

4. Click "Add Visualization" and paste each query link above

### Recommended Layout

**Row 1 (Full Width):**
- Query 6978007: Token Launch Overview (Bar Chart)

**Row 2 (Text Block):**
```markdown
## 🚨 Detection Methodology

**RUG Tokens:** Peaked within 10 minutes + crashed by 1 hour
**HEALTHY Tokens:** Still growing at 1 hour + maintained value at 4 hours

**Key Risk Signals:**
- 🔴 VERY HIGH RISK: Buy volume first 10s > 50 SOL AND Sell volume 1m > 15 SOL
- 🟡 HIGH RISK: Either threshold exceeded
- 🟠 MODERATE RISK: Buy volume first 10s > 30 SOL
```

**Row 3 (50/50 Split):**
- Left: Query 6978009 - Rugpull Risk Signals (Table)
- Right: Query 6978012 - Daily Trend (Line Chart)

**Row 4 (Full Width):**
- Query 6978008: High-Risk Token Feed (Table, scrollable)

**Row 5 (50/50 Split):**
- Left: Query 6978010 - Risk Score Model (Scatter Plot)
- Right: Query 6978011 - Serial Creators (Table)

### Visualization Settings

**Query 6978007 (Bar Chart):**
- X-axis: tier
- Y-axis: token_count
- Sort: by tier name
- Show value labels

**Query 6978008 (Table):**
- Sort by: buy_sol_vol_10s DESC
- Conditional formatting: 
  - risk_level "🔴 VERY HIGH RISK" → Red background
  - risk_level "🟡 HIGH RISK" → Yellow background

**Query 6978009 (Table):**
- Highlight rows where label = "RUG" in red

**Query 6978010 (Scatter Plot):**
- X: max_mcap (log scale)
- Y: risk_score
- Color by: actual_label
  - CONFIRMED_RUG → Red
  - CONFIRMED_HEALTHY → Green
  - UNKNOWN → Gray

**Query 6978011 (Table):**
- Sort by: rug_count DESC
- Conditional formatting on rug_rate_pct:
  - > 60% → Red
  - 30-60% → Orange
  - < 30% → Yellow

**Query 6978012 (Line Chart):**
- X: launch_date
- Y: rug_rate_pct, healthy_rate_pct (two lines)
- Colors: Red for rug_rate, Green for healthy_rate

## Running Queries Manually

```bash
# Run any query and export results
dune query run 6978007 --output results.csv

# Or directly from SQL file
dune query --query-file queries/query1_overview.sql
```

## API Access

```bash
# Using Dune API
curl -X GET \
  "https://api.dune.com/api/v1/query/6978007/results" \
  -H "X-Dune-API-Key: YOUR_API_KEY"
```

## Next Steps

Once the dashboard is live:
1. Share the dashboard URL: `https://dune.com/your_username/pumpfun-rugpull-detector`
2. Embed individual charts on websites using Dune's embed feature
3. Set up scheduled refreshes (if using live data pipeline)
4. Fork queries to customize thresholds for your risk tolerance
