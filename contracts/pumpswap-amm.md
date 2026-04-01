# PumpSwap AMM Contract

## Program ID
`pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`

## Overview

PumpSwap is pump.fun's native DEX, launched **March 20, 2025** to replace Raydium as the graduation destination. It's a **constant product AMM** similar to Uniswap V2.

### Key Facts
- 9 independent security audits completed
- Plans to open-source the code
- All graduated pump.fun tokens now migrate here
- Admin: `8LWu7QM2dGR1G8nKDHthckea57bkCzXyBTAKPJUBDHo8`

## Pool Structure

**Size**: 244 bytes

### Pool Account Fields
- `base_mint` — Token mint address
- `quote_mint` — SOL (or other quote token)
- `lp_mint` — LP token mint
- Pool token accounts (base, quote)
- `lp_supply` — Total LP tokens
- Pool liquidity owner: `7jVYY8nUjbt5gzLt3tZJaHD9NSMyaTuvPhJLfazmjjyy`

## Instructions

### create_pool
```
create_pool(index: u16, base_amount_in: u64, quote_amount_in: u64)
```
Creates a new trading pool with initial liquidity.

### buy
```
buy(base_amount_out: u64, max_quote_amount_in: u64)
```
Buy tokens with SOL (slippage protection via max_quote_amount_in).

### sell
```
sell(base_amount_in: u64, min_quote_amount_out: u64)
```
Sell tokens for SOL (slippage protection via min_quote_amount_out).

### deposit
Add liquidity to a pool. Receives LP tokens.

### withdraw
Remove liquidity from a pool. Burns LP tokens.

### create_config
Set fee rates and fee recipients.

### disable
Emergency stop function with per-function granularity.

## Fee Structure (Tiered)

| SOL Market Cap | Creator | Protocol | LP | Total |
|---------------|---------|----------|-----|-------|
| 0 - 420 | 0.300% | 0.930% | 0.020% | 1.250% |
| 420 - 1,470 | 0.950% | 0.050% | 0.200% | 1.200% |
| 1,470 - 4,200 | 0.300% | 0.050% | 0.200% | 0.550% |
| 4,200 - 98,240 | 0.100% | 0.050% | 0.200% | 0.350% |
| >98,240 | 0.050% | 0.050% | 0.200% | 0.300% |

## Why PumpSwap?

Before PumpSwap, pump.fun tokens graduated to **Raydium**, which meant:
- 6 SOL migration fee (paid by the protocol/users)
- Raydium captured all post-graduation trading fees
- No vertical integration

PumpSwap solved all three:
1. Migration fee reduced to 0.015 SOL
2. pump.fun captures post-graduation trading fees
3. Full vertical integration: creation → trading → DEX

**Impact on Raydium**: RAY token dropped 20% when PumpSwap was announced. Raydium launched LaunchLab the day before PumpSwap as a defensive move.

## Sources
- pump-fun/pump-public-docs
- The Block, DefiLlama
