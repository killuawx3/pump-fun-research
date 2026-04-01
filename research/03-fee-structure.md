# pump.fun — Fee Structure

## Current Fee Structure (as of 2026)

### Token Creation
**0 SOL** (free) — reduced from original 0.02 SOL

### Graduation Fee
**0.015 SOL** (fixed, taken from liquidity) — reduced from original 6 SOL

### Bonding Curve Trading Fees (Pre-Graduation)

| Fee Type | Rate |
|----------|------|
| Creator Fee | 0.300% |
| Protocol Fee | 0.950% |
| LP Fee | 0% |
| **Total** | **1.25%** |

### PumpSwap Fees (Post-Graduation) — Tiered by Market Cap

| SOL Market Cap | Creator Fee | Protocol Fee | LP Fee | Total |
|---------------|-------------|--------------|--------|-------|
| 0 - 420 SOL | 0.300% | 0.930% | 0.020% | 1.250% |
| 420 - 1,470 SOL | 0.950% | 0.050% | 0.200% | 1.200% |
| 1,470 - 4,200 SOL | 0.300% | 0.050% | 0.200% | 0.550% |
| 4,200 - 98,240 SOL | 0.100% | 0.050% | 0.200% | 0.350% |
| >98,240 SOL | 0.050% | 0.050% | 0.200% | 0.300% |

**Key insight**: Fees decrease progressively as market cap grows. Large-cap tokens pay only 0.3% total.

### Creator Fees
- Introduced **May 13, 2025**
- Creators earn trading fees on their tokens
- "Cashback Coins" option: creators can refund all fees to traders instead
- One-time cap on creator fee wallet changes (March 2026, prevents manipulation)

## Historical Fee Evolution

| Period | Creation | Trading | Migration | Notes |
|--------|----------|---------|-----------|-------|
| Jan 2024 (launch) | 0.02 SOL | 1% | 6 SOL | To Raydium |
| Mid-2024 | 0.02 SOL | 1% | 6 SOL | Creator got 0.5 SOL on graduation |
| Mar 2025 (PumpSwap) | 0 SOL | 1% | 0 SOL | Migration fee eliminated |
| May 2025 (Creator fees) | 0 SOL | ~1.25% | 0.015 SOL | Creator fees introduced |
| Current (2026) | 0 SOL | Tiered | 0.015 SOL | Tiered PumpSwap fees |

## Fee Revenue Impact

The fee changes dramatically affected economics:
1. **6 SOL → 0 SOL migration fee**: Increased graduation incentive
2. **Creator fees**: Incentivizes token creators to promote their tokens
3. **Tiered PumpSwap fees**: Competitive with other DEXs for large tokens
4. **Free creation**: Lowered barrier → more token launches (but also more spam)

## Sources
- pump.fun/docs/fees (official)
- Oak Research
- The Block
