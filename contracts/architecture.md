# pump.fun — Smart Contract Architecture

## Three On-Chain Programs

pump.fun operates through three distinct Solana programs:

```
┌─────────────────────────────────────────┐
│           pump.fun Platform             │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────────────┐               │
│  │  Pump Program        │               │
│  │  (Bonding Curve)     │  Token create │
│  │  6EF8rrect...F6P     │──→ Buy/Sell   │
│  │                      │──→ Graduation │
│  └──────────┬───────────┘               │
│             │ migrate                   │
│             ▼                           │
│  ┌──────────────────────┐               │
│  │  PumpSwap AMM        │               │
│  │  pAMMBay6...XEA      │  Post-grad    │
│  │                      │──→ Trading    │
│  │                      │──→ LP mgmt    │
│  └──────────────────────┘               │
│                                         │
│  ┌──────────────────────┐               │
│  │  Pump Fees           │               │
│  │  pfeeUxB6...VZ       │  Fee routing  │
│  │                      │──→ Creator    │
│  │                      │──→ Protocol   │
│  └──────────────────────┘               │
│                                         │
│  ┌──────────────────────┐               │
│  │  Mayhem Program      │  Optional     │
│  │  MAyhSmz...MD4e      │──→ Special    │
│  │                      │    pricing    │
│  └──────────────────────┘               │
│                                         │
└─────────────────────────────────────────┘
```

## Program Details

### Program 1: Pump (Bonding Curve)
- **Program ID**: `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`
- **Purpose**: Token creation, bonding curve trading, graduation
- **Same ID on Mainnet and Devnet**

### Program 2: PumpSwap AMM
- **Program ID**: `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`
- **Purpose**: Post-graduation trading (constant product AMM similar to Uniswap V2)
- **9 independent security audits completed**

### Program 3: Pump Fees
- **Program ID**: `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`
- **Purpose**: Fee routing (creator fees, protocol fees)

### Optional: Mayhem Program
- **Program ID**: `MAyhSmzXzV1pTf7LsNkrNwkWKTo4ougAJ1PPg47MD4e`
- **Purpose**: Special pricing dynamics for "Mayhem mode" tokens
- **8 dedicated fee recipient accounts**

## Token Standard Evolution

| Period | Standard | Instruction |
|--------|----------|-------------|
| Jan 2024 - Nov 2025 | SPL Token + Metaplex | `create` |
| Nov 2025 - Present | Token2022 | `create_v2` |

The migration to Token2022 enables:
- Transfer Hooks (custom logic on transfers)
- Extended metadata without Metaplex dependency
- Future extensibility

## GitHub Repositories

| Repo | Description | Stars |
|------|-------------|-------|
| [pump-public-docs](https://github.com/pump-fun/pump-public-docs) | IDL files for all 3 programs, SDK docs | 386 |
| [carbon](https://github.com/pump-fun/carbon) | Solana indexing framework (fork of sevenlabs-hq) | Active |
| [pump-fun-skills](https://github.com/pump-fun/pump-fun-skills) | AI agent integration skills | - |
| [transfer-hook-authority](https://github.com/pump-fun/transfer-hook-authority) | Token2022 Transfer Hook impl | 1 commit |
| [pump-segments-sdk](https://github.com/pump-fun/pump-segments-sdk) | Profile segments SDK (devnet) | - |
| [react-native-pager-view](https://github.com/pump-fun/react-native-pager-view) | Mobile app fork | - |

## Sources
- github.com/pump-fun (all repos)
- pump.fun official documentation
