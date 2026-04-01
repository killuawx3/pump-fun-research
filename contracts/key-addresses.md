# Key Addresses & Program IDs

## Programs

| Program | ID | Network |
|---------|----|---------|
| **Pump (Bonding Curve)** | `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P` | Mainnet + Devnet |
| **PumpSwap AMM** | `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA` | Mainnet |
| **Pump Fees** | `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ` | Mainnet |
| **Mayhem Program** | `MAyhSmzXzV1pTf7LsNkrNwkWKTo4ougAJ1PPg47MD4e` | Mainnet |

## Key Accounts

| Account | Address | Type |
|---------|---------|------|
| Global State PDA | `4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf` | PDA (seeds: ["global"]) |
| Authority | `FFWtrEQ4B4PKQoVuHYzZq8FabGkVatYzDpEVHsK5rrhF` | - |
| Fee Recipient | `62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV` | - |
| AMM Admin | `8LWu7QM2dGR1G8nKDHthckea57bkCzXyBTAKPJUBDHo8` | - |
| Pool Liquidity Owner | `7jVYY8nUjbt5gzLt3tZJaHD9NSMyaTuvPhJLfazmjjyy` | - |

## Token

| Token | Address |
|-------|---------|
| PUMP Token Mint | `pumpCmXqMfrsAkQ5r49WcJnRayYRqmXz6ae8H7H9Dfn` |

## Mayhem Fee Recipients

Used randomly when a token is in Mayhem mode:

| # | Address |
|---|---------|
| 1 | `GesfTA3X2arioaHp8bbKdjG9vJtskViWACZoYvxp4twS` |
| 2 | `4budycTjhs9fD6xw62VBducVTNgMgJJ5BgtKq7mAZwn6` |
| 3 | `8SBKzEQU4nLSzcwF4a74F2iaUDQyTfjGndn6qUWBnrpR` |
| 4 | `4UQeTP1T39KZ9Sfxzo3WR5skgsaP6NZa87BAkuazLEKH` |
| 5 | `8sNeir4QsLsJdYpc9RZacohhK1Y5FLU3nC5LXgYB4aa6` |
| 6 | `Fh9HmeLNUMVCvejxCtCL2DbYaRyBFVJ5xrWkLnMH6fdk` |
| 7 | `463MEnMeGyJekNZFQSTUABBEbLnvMTALbT6ZmsxAbAdq` |
| 8 | `6AUH3WEHucYZyC61hqpqYUWVto5qA5hjHuNQ32GNnNxA` |

## PDA Derivation

### Bonding Curve PDA
```
seeds = ["bonding-curve", token_mint_pubkey]
program = 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P
```

### Global State PDA
```
seeds = ["global"]
program = 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P
```

## Explorer Links

- **Pump Program**: [Solscan](https://solscan.io/account/6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P)
- **PumpSwap**: [Solscan](https://solscan.io/account/pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA)
- **Helius Orb**: Tags all 3 pump.fun programs
