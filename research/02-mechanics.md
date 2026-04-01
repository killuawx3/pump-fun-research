# pump.fun — Bonding Curve Mechanics & Pricing

## Bonding Curve Model

pump.fun uses a **Constant Product Market Maker (CPAMM)** — the same `x * y = k` formula used by Uniswap, but with **virtual reserves** that set the initial price floor.

### Key Parameters

| Parameter | Value |
|-----------|-------|
| Total Token Supply | 1,000,000,000 (1B tokens, 6 decimals) |
| Virtual SOL Reserves (initial) | 30 SOL |
| Virtual Token Reserves (initial) | 1,073,000,191 tokens |
| Real Token Reserves (on curve) | 793,100,000 tokens |
| Reserved for LP Migration | ~206,900,000 tokens (~20%) |
| Constant k | 30 × 1,073,000,191 = 32,190,005,730 |

### The Pricing Formula

```
Price per token = virtual_sol_reserves / virtual_token_reserves

Tokens received for x SOL:
y = 1,073,000,191 - (32,190,005,730 / (30 + x))

Where:
  x = SOL invested
  y = tokens received
  k = 32,190,005,730 (constant product)
```

### Price Trajectory

| Stage | Price (SOL/token) | Multiple |
|-------|-------------------|----------|
| Initial | ~0.000000028 | 1x |
| King of the Hill (~50%) | ~0.00000012 | ~4.3x |
| Graduation (100%) | ~0.00000041 | ~14.64x |

### Bonding Curve Progress

```
progress = ((1,073,000,000 × 10^6) - virtualTokenReserves) × 100 / (793,100,000 × 10^6)
```

Or equivalently:
```
progress = 100 - (((token_balance - 206,900,000) × 100) / 793,100,000)
```

## Token Creation Process

### Current (create_v2 — Token2022)
1. User provides: name, symbol, image (uploaded to IPFS/Arweave)
2. Token mint created using **Token2022** standard (since Nov 2025)
3. Metaplex metadata attached
4. 1B tokens minted → 793.1M placed on bonding curve
5. Bonding curve PDA created: seeds = ["bonding-curve", mint_pubkey]
6. **Cost: 0 SOL** (free creation)

### Legacy (create — SPL Token)
- Used standard SPL token program
- Deprecated after Token2022 migration
- Originally cost 0.02 SOL

## Trading Mechanics

### Buy
- User sends SOL → receives tokens from bonding curve
- `buy(amount, max_sol_cost)` — slippage protection via max_sol_cost
- Virtual SOL reserves increase, virtual token reserves decrease
- Price rises along the curve

### Sell
- User sends tokens → receives SOL from bonding curve
- `sell(amount, min_sol_output)` — slippage protection via min_sol_output
- Virtual token reserves increase, virtual SOL reserves decrease
- Price falls along the curve

## Graduation (Migration to PumpSwap)

When the bonding curve reaches 100% completion:

1. **Trigger**: All 793.1M sellable tokens purchased (~85 SOL total raised)
2. **Market Cap at Graduation**: ~410 SOL (~$69,000 USD)
3. **Migration**: ~79 SOL paired with ~206.9M reserved tokens
4. **LP Pool Created**: On PumpSwap (previously Raydium)
5. **LP Tokens Burned**: Permanently locked, no rug pull possible
6. **Fee**: 0.015 SOL (down from original 6 SOL)
7. **Permission**: Permissionless — anyone can trigger the `migrate` instruction

### "King of the Hill"

When a token's bonding curve reaches **~50% completion** (~45 SOL raised, ~$30K market cap):
- Token gets featured prominently on pump.fun homepage
- Significant social proof / visibility boost
- Often triggers additional buying pressure

## Graduation Rate

| Period | Graduation Rate |
|--------|----------------|
| Historical Average | ~1.0-1.7% |
| Low Point | ~0.58% |
| High Point | ~2.01% |
| **98.5% of tokens never graduate** | |

## Mayhem Mode (Nov 2025+)

A special mode for bonding curves with "unpredictable pricing dynamics":
- Boolean flag `is_mayhem_mode` on bonding curve accounts
- Requires special fee recipient accounts (Mayhem program)
- Program ID: `MAyhSmzXzV1pTf7LsNkrNwkWKTo4ougAJ1PPg47MD4e`

## Sources
- Solana Stack Exchange (bonding curve analysis)
- pump.fun official documentation
- Binance Square technical breakdowns
- Medium/Substack bonding curve research
