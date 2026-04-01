# SDKs & Developer Tools

## Official SDKs (npm)

| Package | Version | Purpose |
|---------|---------|---------|
| `@pump-fun/pump-sdk` | v1.32.0 | Coin creation, trading, fee management |
| `@pump-fun/pump-swap-sdk` | v1.14.1 | PumpSwap AMM interactions |
| `@pump-fun/agent-payments-sdk` | - | AI agent payment integration |

### Basic Usage Pattern

```typescript
import { PumpSdk } from '@pump-fun/pump-sdk';

const sdk = new PumpSdk(connection);
const global = await sdk.fetchGlobal();

// Create token
await sdk.createAndBuyInstructions({
  global, mint, name, symbol, uri, creator, user, solAmount, amount
});

// Buy tokens
const buyState = await sdk.fetchBuyState(mint, user);

// Sell tokens
const sellState = await sdk.fetchSellState(mint, user);
```

## Community SDKs

### TypeScript/JavaScript
| Package | Description |
|---------|-------------|
| `@nirholas/pump-sdk` | Full-featured SDK + MCP server + Telegram bot + dashboards |
| `rckprtr/pumpdotfun-sdk` | Popular early SDK (somewhat outdated due to IDL changes) |
| `Erbsensuppee/pumpfun-pumpswap-sdk` | Combined bonding curve + AMM |
| `wsy2220/pump-swap-sdk` | Fork of official pump-swap-sdk |

### Rust
| Package | Description |
|---------|-------------|
| `nhuxhr/pumpfun-rs` (v4.6.0) | Rust SDK on crates.io |

### Python
| Package | Description |
|---------|-------------|
| `pump_fun_py` | Buy/sell functions, 313 stars |
| `pumpswapamm` (PyPI) | PumpSwap AMM SDK |
| `pumpfun-research` | Wallet analysis, PnL, Helius integration |

## Indexing & Data Tools

### Carbon (Official)
**Repo**: github.com/pump-fun/carbon
- Solana indexing framework
- Pipeline: datasources → decoders → processors
- Pre-built decoders for pump.fun, Raydium, Jupiter, Orca
- CLI to generate custom decoders from IDL files
- Supports: RPC block subscribe, Helius Atlas WS, Yellowstone gRPC

### Community Data Tools
| Tool | Description |
|------|-------------|
| `pumpfun-grpc-sniper` | Yellowstone gRPC sniping toolkit |
| `gRPC-pumpfun-new-token-track` | New token launch tracker |
| `pump-fun-bot` (Chainstack) | Educational bot example |
| `BankkRoll/pumpfun-apis` | 483 unofficial API endpoints documented |

## RPC Methods for Data Access

| Method | Use Case |
|--------|----------|
| `getAccountInfo` | Fetch bonding curve state for any token |
| `getProgramAccounts` | Query all accounts owned by pump.fun program |
| `logsSubscribe` | Real-time monitoring of creates/buys/sells |
| `getSignaturesForAddress` | Transaction history for program or account |
