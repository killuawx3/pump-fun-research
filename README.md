# pump.fun Deep Research & Analysis

A comprehensive research repository analyzing **pump.fun** — the dominant Solana memecoin launchpad that has generated over $1B in cumulative revenue and launched 17.5M+ tokens since January 2024.

## Repository Structure

```
pump-fun-research/
├── research/
│   ├── 01-overview.md              # Platform overview & history
│   ├── 02-mechanics.md             # Bonding curve, pricing, graduation
│   ├── 03-fee-structure.md         # Complete fee breakdown
│   ├── 04-revenue-analysis.md      # Revenue model & financials
│   ├── 05-competition.md           # Competitive landscape
│   └── 06-pump-token.md            # PUMP token & ICO
├── contracts/
│   ├── architecture.md             # Smart contract architecture
│   ├── bonding-curve.md            # Bonding curve contract deep dive
│   ├── pumpswap-amm.md             # PumpSwap AMM contract
│   ├── key-addresses.md            # All program IDs & key accounts
│   └── sdks-and-tools.md           # Official & community SDKs
├── data/
│   ├── sources.md                  # Data source reference guide
│   ├── dune-dashboards.md          # Best Dune Analytics dashboards
│   ├── apis.md                     # Official & unofficial APIs
│   └── extracted/                  # Raw extracted data files
├── analysis/
│   ├── key-metrics.md              # Key statistics & metrics
│   ├── graduation-analysis.md      # Token graduation rate analysis
│   ├── market-dynamics.md          # Market share & volume trends
│   └── charts/                     # Generated visualizations
├── presentation/
│   └── pump-fun-analysis.md        # Presentation-ready summary
└── scripts/
    └── data_extraction.py          # Data extraction scripts
```

## Key Findings

| Metric | Value |
|--------|-------|
| Launch Date | January 19, 2024 |
| Total Tokens Created | ~17.5 million |
| Graduation Rate | ~1.0-1.7% |
| Cumulative Revenue | ~$1.02 billion |
| Cumulative DEX Volume | ~$87 billion |
| Daily Active Users | ~114,400 |
| Total Unique Addresses | 32.2 million |
| PUMP Token ICO | $1.32 billion raised |
| Peak Daily Revenue | $15.5M (Jan 2025) |

## How pump.fun Works (TL;DR)

1. **Create** — Anyone creates a token for free (name, symbol, image)
2. **Trade** — 800M tokens placed on a bonding curve (constant product AMM)
3. **Graduate** — When ~85 SOL is raised (~$69K market cap), token auto-migrates to PumpSwap DEX
4. **LP Burned** — Liquidity is permanently locked (no rug pulls possible)

## Smart Contract Programs

| Program | ID |
|---------|-----|
| Pump (Bonding Curve) | `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P` |
| PumpSwap AMM | `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA` |
| Pump Fees | `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ` |

## Data Sources

- **Dune Analytics**: [Main Dashboard](https://dune.com/adam_tehc/pumpfun)
- **DefiLlama**: [pump.fun Protocol](https://defillama.com/protocol/pump.fun)
- **Token Terminal**: [pump.fun Metrics](https://tokenterminal.com/explorer/projects/pumpfun)
- **Bitquery**: [PumpFun API](https://docs.bitquery.io/docs/blockchain/Solana/PumpFun/)

---

*Research conducted April 2026*
