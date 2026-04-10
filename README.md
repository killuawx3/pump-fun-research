# Pump.fun Rugpull Detector

Research project analyzing pump-and-dump patterns on pump.fun using on-chain volume signals.

## 📊 Dune Dashboard

**Status:** Setup guide ready, queries prepared  
**Setup Instructions:** [`DUNE_DASHBOARD_SETUP.md`](DUNE_DASHBOARD_SETUP.md)

### Dashboard Components

1. **Token Launch Overview** - Distribution by market cap tier
2. **Rug vs Healthy Signals** - Volume pattern comparison
3. **Live High-Risk Feed** - Real-time flagged tokens (7 days)
4. **Risk Scoring Model** - Automated classification with validation
5. **Daily Trend** - 30-day rugpull rate timeseries
6. **Creator Tracker** - Serial bad actor detection

All queries are in [`queries/`](queries/) directory.

## 📈 Key Findings

### Classification Methodology

**RUG (n=163):** Peaked within 10min + crashed by 1hr  
**HEALTHY (n=45):** Growing at 1hr + maintained at 4hr

### Strongest Signals

| Signal | RUG Median | HEALTHY Median | Ratio |
|--------|------------|----------------|-------|
| Buy Volume (first 10s) | 34.41 SOL | 5.09 SOL | **6.8x** |
| Sell Volume (first 1m) | 19.74 SOL | 2.79 SOL | **7.1x** |
| 1H Retention | 2.8% | 19.3% | **6.9x** |

### Risk Thresholds

- 🔴 **VERY HIGH RISK:** `buy_vol_10s > 50 SOL` AND `sell_vol_1m > 15 SOL`
- 🟡 **HIGH RISK:** Either threshold exceeded
- 🟠 **MODERATE RISK:** `buy_vol_10s > 30 SOL`

## 📁 Repository Structure

```
pump-fun-rugpull-detector/
├── REPORT.md              # Full research report (English)
├── REPORT-KR.md           # Korean translation
├── DUNE_DASHBOARD_SETUP.md  # Dashboard creation guide
├── dune-queries.sql       # All queries in one file
├── queries/               # Individual query files
│   ├── query1_overview.sql
│   ├── query2_signals.sql
│   ├── query3_highrisk.sql
│   ├── query4_scoring.sql
│   ├── query5_trend.sql
│   └── query6_creators.sql
├── charts/                # Analysis visualizations
├── data/                  # Raw datasets
└── PLAN.md                # Original research plan
```

## 🔧 Data Source

**Table:** `dune.bumaye17.result_clean_pump_fun`  
**Sample:** 47,247 tokens launched on January 5, 2025  
**Note:** Historical dataset. For live tracking, see setup guide for pipeline instructions.

## 🚀 Quick Start

### Option 1: Create Dune Dashboard (Recommended)

1. Read [`DUNE_DASHBOARD_SETUP.md`](DUNE_DASHBOARD_SETUP.md)
2. Copy queries from `queries/` to Dune
3. Configure visualizations as described
4. Assemble dashboard

### Option 2: Run Queries Locally (Dune CLI)

```bash
# Install Dune CLI
curl -L https://github.com/duneanalytics/cli/releases/download/v0.1.9/dune_darwin_arm64 -o dune
chmod +x dune && mv dune ~/.local/bin/

# Authenticate
dune auth

# Run any query
dune query --query-file queries/query1_overview.sql
```

## 📝 Research Report

Full analysis with case studies, trade-by-trade breakdowns, and charts:
- English: [`REPORT.md`](REPORT.md)
- Korean: [`REPORT-KR.md`](REPORT-KR.md)

## 🎯 Use Cases

1. **Traders:** Pre-screen new launches before buying
2. **Researchers:** Study pump-and-dump mechanics at scale
3. **Platform Operators:** Detect and flag suspicious launches
4. **Investigators:** Track serial bad actors across wallets

## ⚠️ Limitations

1. **Historical Data:** Current dataset is January 5, 2025 only
2. **No Wallet Clustering:** Doesn't track if snipers are same wallets
3. **Post-Graduation Blind Spot:** Only tracks bonding curve phase
4. **No Social Signals:** Doesn't incorporate Twitter/Telegram activity

## 🛠️ Next Steps

- [ ] Real-time pipeline for live detection
- [ ] Wallet clustering for serial creator detection
- [ ] Social signal integration (Twitter/Telegram)
- [ ] ML classifier training on labeled dataset
- [ ] Telegram alert bot integration
- [ ] Post-graduation tracking (PumpSwap/Raydium)

## 📊 Sample Statistics

From 47,247 tokens analyzed:
- **42.3%** dead on arrival (< $7K mcap)
- **48.9%** low traction ($7K-$20K)
- **Only 0.2%** reached $1M+ mcap
- **91.2%** never exceeded $20K mcap

## 📧 Contact

For questions or collaboration:
- GitHub Issues: [Open an issue](https://github.com/killuawx3/pump-fun-research/issues)
- Research Report: See REPORT.md for methodology details

---

**Research Date:** April 3, 2026  
**Data Source:** Dune Analytics - pumpdotfun_solana tables  
**Classification:** 163 RUG tokens, 45 HEALTHY tokens (self-labeled)
