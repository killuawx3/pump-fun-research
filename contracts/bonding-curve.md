# Bonding Curve Contract — Deep Dive

## Program ID
`6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`

## Global State Account

**PDA**: `4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf`
**Seeds**: `["global"]`

### Global Parameters

| Parameter | Value |
|-----------|-------|
| Authority | `FFWtrEQ4B4PKQoVuHYzZq8FabGkVatYzDpEVHsK5rrhF` |
| Fee Recipient | `62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV` |
| initial_virtual_token_reserves | 1,073,000,000,000,000 (with 6 decimals) |
| initial_virtual_sol_reserves | 30,000,000,000 (30 SOL in lamports) |
| initial_real_token_reserves | 793,100,000,000,000 (with 6 decimals) |
| token_total_supply | 1,000,000,000,000,000 (1B tokens, 6 decimals) |
| fee_basis_points | 100 (1% fee on buy/sell) |
| pool_migration_fee | 15,000,001 lamports (~0.015 SOL) |

## Bonding Curve Account (Per Token)

**PDA Seeds**: `["bonding-curve", mint_pubkey]`
**Size**: 82 bytes

### Account Layout

| Offset | Field | Type | Description |
|--------|-------|------|-------------|
| 0x00-0x07 | discriminator | [u8; 8] | SHA256("account:BondingCurve")[:8] |
| 0x08 | virtual_token_reserves | u64 | Current virtual token reserves |
| 0x10 | virtual_sol_reserves | u64 | Current virtual SOL reserves |
| 0x18 | real_token_reserves | u64 | Actual tokens remaining on curve |
| 0x20 | real_sol_reserves | u64 | Actual SOL in the curve |
| 0x28 | token_total_supply | u64 | Total token supply (1B) |
| 0x30 | complete | bool | Whether curve has graduated |
| 0x31 | is_mayhem_mode | bool | Mayhem mode flag (added Nov 2025) |
| 0x32 | creator | Pubkey | Token creator address |

**Note**: Size was 81 bytes before Mayhem mode addition.

## Instructions

### create (DEPRECATED)
Creates a new token using SPL Token + Metaplex metadata.

### create_v2 (Current)
Creates a new token using Token2022 standard.
- Mints 1B tokens
- Places 793.1M on bonding curve
- Creates metadata
- Sets up bonding curve PDA

### buy
```
buy(amount: u64, max_sol_cost: u64)
```
- `amount`: number of tokens to buy
- `max_sol_cost`: maximum SOL willing to pay (slippage protection)
- Updates virtual and real reserves
- Emits trade event

### sell
```
sell(amount: u64, min_sol_output: u64)
```
- `amount`: number of tokens to sell
- `min_sol_output`: minimum SOL to receive (slippage protection)
- Updates virtual and real reserves
- Emits trade event

### migrate
```
migrate()
```
- **Permissionless** — anyone can call once curve is complete
- **Idempotent** — safe to call multiple times
- Transfers SOL and remaining tokens to PumpSwap
- Creates LP pool and burns LP tokens

### set_params
- Authority-only instruction
- Updates global configuration

### extend_account
- For future upgrades to account structure

## Pricing Math

### Initial State
```
virtual_sol = 30 SOL
virtual_tokens = 1,073,000,191
k = 30 × 1,073,000,191 = 32,190,005,730
```

### Buy Calculation
```python
def calculate_buy(sol_amount, virtual_sol, virtual_tokens):
    k = virtual_sol * virtual_tokens
    new_virtual_sol = virtual_sol + sol_amount
    new_virtual_tokens = k / new_virtual_sol
    tokens_out = virtual_tokens - new_virtual_tokens
    return tokens_out
```

### Sell Calculation
```python
def calculate_sell(token_amount, virtual_sol, virtual_tokens):
    k = virtual_sol * virtual_tokens
    new_virtual_tokens = virtual_tokens + token_amount
    new_virtual_sol = k / new_virtual_tokens
    sol_out = virtual_sol - new_virtual_sol
    return sol_out
```

### Price at Any Point
```python
price_per_token = virtual_sol_reserves / virtual_token_reserves
# Adjusted for decimals: SOL has 9, tokens have 6
price_in_sol = (virtual_sol_reserves / 1e9) / (virtual_token_reserves / 1e6)
```

## Graduation Mechanics

1. **Trigger**: `real_token_reserves == 0` (all 793.1M tokens purchased)
2. **Total SOL needed**: ~85 SOL
3. **Market cap at graduation**: ~410 SOL (~$69K)
4. **Migration**:
   - ~79 SOL + ~206.9M tokens → PumpSwap LP
   - 0.015 SOL migration fee
   - LP tokens burned automatically

## Sources
- pump-fun/pump-public-docs (IDL files)
- Solana Stack Exchange
- Binance Square technical analysis
