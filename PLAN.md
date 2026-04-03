# Pump.fun Rugpull Early Warning Signal System

## Goal

Build a system that detects and alerts users about likely rugpull tokens on pump.fun BEFORE the dump happens — ideally within the first few minutes of a token's life, when the pump phase is still active. The system analyzes on-chain behavioral patterns extracted from known historical rugpulls and applies them in real-time to new token launches.

## Context & Assumptions

### What We Know From Our Analysis

We pulled Dune on-chain data for 6 notorious rugpull/insider tokens:

| Token | Peak | Drop | Volume | Pattern |
|-------|------|------|--------|---------|
| $LIBRA (Milei) | $2.87 | -94% | $1.9B | Insiders drained LP within hours |
| $HAWK (Hawk Tuah) | $0.013 | -86% | $39M | Snipers + insiders dumped at launch |
| $TRUMP | $71.82 | -98% | $28.7B | Insider bought $5.9M in 1st minute |
| $MELANIA | $11.97 | -81% | $6.5B | 22 wallets sniped in 42 seconds |
| $JENNER (pump.fun) | $0.037 | -100% | $350M | Sahil Arora celeb pump scheme |
| $QUANT (pump.fun) | $0.067 | -99% | $479M | 13yo kid rugged live on stream |

### Available Data Sources on Dune

Decoded pump.fun tables (goldmine):
- `pumpdotfun_solana.pump_evt_createevent` — token creation with creator, mint, symbol, bonding curve, reserves
- `pumpdotfun_solana.pump_evt_tradeevent` — every buy/sell with user, amounts, virtual reserves, fees, is_buy flag
- `pumpdotfun_solana.pump_call_buy` / `pump_call_sell` — individual buy/sell calls
- `pumpdotfun_solana.pump_evt_completeevent` — when bonding curve completes (graduates to Raydium)
- `pumpdotfun_solana.pump_call_migrate` — migration events
- `dex_solana.trades` — DEX trades with USD pricing after graduation
- `dune.bumaye17.result_clean_pump_fun` — community table with mcap snapshots at 10m, 1h, 4h, 12h

### Key Insight from SolRugDetector Paper (arXiv:2603.24625, March 2026)

- 76.4% of 100K Solana tokens in H1 2025 were rugpulls
- Solana rugpulls are NOT about malicious contract code (SPL Token is standard) — they're about BEHAVIORAL patterns: liquidity manipulation, wash trading, coordinated dumping
- Detection must focus on transaction flow analysis, not static code analysis
- Extremely short lifecycles and price-driven dynamics are key signals

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    PHASE 1: RESEARCH                     │
│  Historical pattern extraction from known rugpulls       │
│  using Dune SQL queries on pump.fun decoded tables       │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                 PHASE 2: FEATURE ENGINEERING              │
│  Define quantitative signals from on-chain behavior      │
│  Train/validate on labeled dataset                       │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              PHASE 3: REAL-TIME DETECTOR                  │
│  Solana RPC/WebSocket → Feature extraction → Scoring     │
│  → Alert via Telegram bot                                │
└─────────────────────────────────────────────────────────┘
```

---

## Phase 1: Historical Pattern Extraction (Dune Research)

### Step 1.1: Build Labeled Dataset

Query `pumpdotfun_solana.pump_evt_createevent` + `pump_evt_tradeevent` for:

**Known rugpulls (positive class):**
- LIBRA: `Bo9jh3wsmcC2AjakLWzNmKJ3SgtZmXEcSaW7L2FAvUsU`
- JENNER: `4GJ3TCt5mTgQT5BRKb14AkjddpFQqKVfphxzS3t4foZ9`
- QUANT: `3an8rhdepsLCya22af7qDBKPbdomw8K4iCHXaA2Gpump`
- HAWK: `HAWKThXRcNL9ZGZKqgUXLm4W8tnRZ7U6MVdEepSutj34`
- MELANIA: `FUAfBo2jgks6gB4Z4LfZkqSZgzNucisEHqnNebaRxM1P`
- Plus: scrape rugpull databases, use the community table `result_clean_pump_fun` to find tokens where max_mcap >> last_mcap (e.g., max_mcap/last_mcap > 10x AND max_mcap > $100K)

**Legitimate tokens (negative class):**
- Tokens that graduated bonding curve AND maintained value (BONK, WIF, POPCAT early days, etc.)
- Tokens from `pump_evt_completeevent` that still trade actively months later

**Target: 500+ labeled rugpulls, 500+ legitimate tokens**

### Step 1.2: Extract Behavioral Features Per Token

For each token, compute features from the FIRST N minutes (1min, 5min, 10min, 30min windows) after creation:

**A. Creator Behavior Signals**
1. `creator_first_buy_pct` — What % of initial supply did creator buy?
2. `creator_buy_timing` — How fast after creation did creator buy? (seconds)
3. `creator_prior_tokens` — How many tokens has this creator address launched before? (serial rugger signal)
4. `creator_prior_rug_rate` — Of creator's past tokens, what % crashed >90%?
5. `creator_wallet_age` — How old is the creator wallet? (fresh = suspicious)
6. `creator_funded_by` — Was creator wallet funded by a known wash trading cluster?

**B. Early Trading Pattern Signals (first 1-10 minutes)**
7. `sniper_count_10s` — Number of unique buyers in first 10 seconds (bot signal)
8. `sniper_volume_10s` — SOL volume in first 10 seconds
9. `top_wallet_concentration` — % of supply held by top 5 wallets after 5 min
10. `buy_sell_ratio_5m` — Ratio of buys to sells in first 5 minutes (all buys, no sells = artificial pump)
11. `unique_buyers_5m` — Number of unique buyer addresses in first 5 min
12. `avg_buy_size_sol` — Average buy size (unusually large = insider)
13. `max_single_buy_pct` — Largest single buy as % of supply
14. `wallet_cluster_score` — Are early buyers connected (funded from same source)?

**C. Price/Liquidity Dynamics**
15. `price_velocity_5m` — Price change rate in first 5 minutes (too fast = artificial)
16. `bonding_curve_progress` — How fast is the bonding curve filling? (rushed = suspicious)
17. `virtual_sol_reserves_growth` — Reserve growth trajectory
18. `sell_pressure_ratio` — Once sells begin, ratio of sell volume to accumulated buy volume
19. `first_sell_timing` — How quickly does the first sell happen after buying starts?
20. `price_retracement_from_peak` — Max drawdown from local peak within window

**D. Social/Metadata Signals**
21. `name_similarity_score` — Is name similar to existing famous tokens? (copycat signal)
22. `uri_metadata_quality` — Does the token have proper metadata, image, social links?
23. `symbol_length` — Very short or very long symbols correlate differently

### Step 1.3: Validate Features with Dune Queries

For each feature, write Dune queries against our 6 known rugpulls vs. known legit tokens to verify discriminative power. Example:

```sql
-- Feature: sniper_count in first 10 seconds
SELECT 
  mint,
  COUNT(DISTINCT user) as unique_buyers_10s,
  SUM(CAST(sol_amount AS double)) / 1e9 as sol_volume_10s
FROM pumpdotfun_solana.pump_evt_tradeevent
WHERE mint = '{TOKEN_MINT}'
  AND is_buy = true
  AND evt_block_time <= (
    SELECT MIN(evt_block_time) + INTERVAL '10' SECOND 
    FROM pumpdotfun_solana.pump_evt_tradeevent 
    WHERE mint = '{TOKEN_MINT}'
  )
GROUP BY 1
```

---

## Phase 2: Model & Scoring System

### Step 2.1: Feature Matrix Construction

- Pull all features for the labeled dataset (500 rug + 500 legit) using Dune batch queries
- Export to CSV/parquet
- Clean, normalize, handle nulls

### Step 2.2: Model Options (from simplest to complex)

**Option A: Rule-Based Scoring (Start Here)**
Weighted heuristic score from the most discriminative features:

```python
score = 0
if creator_prior_tokens > 3 and creator_prior_rug_rate > 0.5:
    score += 30  # Serial rugger
if sniper_count_10s > 5:
    score += 15  # Bot army
if top_wallet_concentration > 0.5:
    score += 20  # Whale dominance
if creator_wallet_age < 24_hours:
    score += 15  # Fresh wallet
if buy_sell_ratio_5m > 20:
    score += 10  # No organic selling
if max_single_buy_pct > 0.1:
    score += 10  # Single wallet grabbed >10%

# score > 50 = HIGH RISK, > 30 = MEDIUM RISK
```

Pros: Transparent, explainable, fast, no training infra needed
Cons: May miss complex patterns

**Option B: Gradient Boosted Trees (XGBoost/LightGBM)**
- Train on labeled feature matrix
- SHAP values for explainability
- Cross-validated on time-split data (not random — prevent lookahead)
- Output: probability score 0-1

Pros: Handles feature interactions, better accuracy
Cons: Needs labeled data, potential overfitting

**Option C: Combined**
- Use rule-based for immediate alerts (0-60 seconds post-launch)
- Use ML model for refined scoring (5-10 minutes post-launch when more features available)

### Step 2.3: Backtesting

Run the model on ALL pump.fun tokens from a recent week/month:
- True positive rate: What % of actual rugpulls did we flag?
- False positive rate: What % of legit tokens did we incorrectly flag?
- Early detection rate: How many minutes BEFORE the dump did we flag?
- Target: >80% true positive, <20% false positive, >5 min early warning

---

## Phase 3: Real-Time Detection & Alerting

### Step 3.1: Data Pipeline

```
Solana RPC (WebSocket)
  │
  ├── Subscribe to pump.fun program logs
  │   (program: 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P)
  │
  ├── Parse CreateEvent → new token detected
  │   └── Start monitoring window
  │
  ├── Parse TradeEvent → accumulate features
  │   └── Update running feature vector
  │
  └── At each checkpoint (10s, 1m, 5m, 10m):
      └── Compute score → Alert if threshold exceeded
```

**Tech stack options:**
- **Python + solana-py + websockets** — simple, we can build fast
- **Helius/Shyft webhooks** — managed service, lower infra burden
- **Yellowstone gRPC (Geyser plugin)** — highest performance, most complex

### Step 3.2: Alert System

Telegram bot that sends alerts to a channel:

```
🚨 RUGPULL ALERT — HIGH RISK (score: 78/100)

Token: $SCAMCOIN (mint: Abc...xyz)
Created: 32 seconds ago
Creator: 5th token from this wallet (4 prev rugs)

Signals:
  🔴 Serial rugger (4/4 past tokens crashed >90%)
  🔴 8 sniper bots bought in first 5 seconds
  🔴 Top 3 wallets hold 62% of supply
  🟡 Creator wallet only 2 hours old
  🟡 No metadata URI set

Bonding curve: 12% filled
Current mcap: $45,000

⚠️ DO NOT APE — High probability of rugpull
```

### Step 3.3: Dashboard (Optional)

Simple web dashboard showing:
- Live feed of new pump.fun tokens with risk scores
- Historical accuracy stats
- Leaderboard of serial ruggers
- Token detail view with feature breakdown

---

## Implementation Phases & Timeline

### Phase 1: Research & Feature Validation (Week 1-2)
- [ ] Build labeled dataset from Dune (rugpulls + legit tokens)
- [ ] Write feature extraction queries for all 20+ features
- [ ] Validate feature discriminative power on known cases
- [ ] Extract full feature matrix for labeled dataset
- [ ] Deliverable: CSV with features + labels, feature importance analysis

### Phase 2: Model Development (Week 2-3)
- [ ] Implement rule-based scoring v1
- [ ] Train XGBoost model on labeled data
- [ ] Backtest on 1 month of pump.fun tokens
- [ ] Tune thresholds for precision/recall tradeoff
- [ ] Deliverable: Scoring model with >80% accuracy, backtest report

### Phase 3: Real-Time Pipeline (Week 3-4)
- [ ] Set up Solana WebSocket listener for pump.fun events
- [ ] Implement real-time feature computation
- [ ] Build Telegram alert bot
- [ ] Run in shadow mode (score but don't alert) for 1 week
- [ ] Go live with alerts
- [ ] Deliverable: Running Telegram bot with live alerts

### Phase 4: Iteration (Ongoing)
- [ ] Monitor false positive/negative rates
- [ ] Add new features based on emerging scam patterns
- [ ] Build web dashboard
- [ ] Consider expanding to other launchpads (Moonshot, etc.)

---

## Key Technical Decisions

### 1. Where to run feature extraction?

| Option | Latency | Cost | Complexity |
|--------|---------|------|------------|
| Dune queries (batch) | Minutes | API credits | Low |
| Direct Solana RPC | Seconds | RPC costs | Medium |
| Helius webhooks | ~1-2s | $50-200/mo | Low |
| Geyser gRPC (Yellowstone) | ~200ms | Self-hosted node | High |

**Recommendation:** Start with Helius webhooks for real-time, Dune for historical research and backtesting.

### 2. Alert latency target

- First alert: within 30-60 seconds of token creation (rule-based, limited features)
- Refined alert: within 5-10 minutes (ML model, full feature set)
- Most rugpulls we analyzed peaked within 1-2 HOURS, so even 10-minute alerts give significant warning

### 3. False positive management

- Tiered alerts: HIGH (>70 score), MEDIUM (40-70), LOW (20-40)
- Only push notifications for HIGH
- Include reasoning so users can evaluate themselves
- Track accuracy publicly for trust

---

## Open Questions

1. **Labeled data size** — Is 500+500 enough or do we need thousands? The community table `result_clean_pump_fun` may help scale this up quickly.

2. **Creator wallet clustering** — Should we build a wallet graph to identify connected addresses? This requires off-Dune infra but could be the strongest signal.

3. **Graduated vs. pre-graduation** — Should we only alert during bonding curve phase, or also after graduation to Raydium? Different dynamics.

4. **Legal/ethical** — Publishing "this is a scam" alerts carries liability risk. Frame as "risk score" not "scam detection"?

5. **Adversarial adaptation** — Scammers will adapt once they know our signals. How do we handle:
   - Using multiple fresh wallets instead of one serial rugger
   - Delaying the dump to avoid early sell pattern detection
   - Simulating organic trading before dumping

---

## References

- SolRugDetector paper: arXiv:2603.24625 (March 2026) — 76.4% of Solana tokens are rugpulls
- SolRPDS Dataset: First public Solana rug pull labeled dataset
- Our data: 6 token case studies with hourly Dune data (LIBRA, HAWK, TRUMP, MELANIA, JENNER, QUANT)
- Pump.fun decoded tables on Dune: `pumpdotfun_solana.*`
- pump.fun program ID: `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`
