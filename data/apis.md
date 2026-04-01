# pump.fun APIs — Complete Reference

## Official pump.fun Internal APIs

Source: github.com/BankkRoll/pumpfun-apis (483 endpoints documented)

### Base URLs

| API | URL |
|-----|-----|
| Frontend API v3 | `https://frontend-api-v3.pump.fun/` |
| Advanced Analytics v2 | `https://advanced-api-v2.pump.fun/` |
| Profile API | `https://profile-api.pump.fun` |
| Swap API | `https://swap-api.pump.fun` |
| Volatility API | `https://volatility-api-v2.pump.fun` |
| Market API | `https://market-api.pump.fun` |
| Clips API | `https://clips-api.pump.fun` |

### Authentication
Most endpoints require JWT auth with header:
```
Origin: https://pump.fun
```

OpenAPI specs available in the BankkRoll/pumpfun-apis repo.

### Notable Endpoints (Frontend API v3)

```
GET /coins/trending          - Trending tokens
GET /coins/king-of-the-hill  - Tokens near 50% curve
GET /coins/{mint}           - Token details
GET /coins/{mint}/trades    - Recent trades
GET /coins/recently-created - New tokens
```

## Third-Party APIs

### Bitquery GraphQL

**IDE**: https://ide.bitquery.io/
**Docs**: https://docs.bitquery.io/docs/blockchain/Solana/PumpFun/

#### Example: Get Recent pump.fun Trades
```graphql
{
  Solana {
    DEXTrades(
      where: {
        Trade: {
          Dex: {
            ProtocolName: { is: "pump" }
          }
        }
      }
      limit: { count: 10 }
      orderBy: { descending: Block_Time }
    ) {
      Trade {
        Buy { Amount Currency { Symbol MintAddress } }
        Sell { Amount Currency { Symbol MintAddress } }
        Dex { ProtocolName }
      }
      Block { Time }
    }
  }
}
```

#### Example: New Token Launches (Subscription)
```graphql
subscription {
  Solana {
    DEXTrades(
      where: {
        Trade: {
          Dex: { ProtocolName: { is: "pump" } }
        }
        Transaction: { Result: { Success: true } }
      }
    ) {
      Trade {
        Buy { Currency { Symbol MintAddress Name } }
      }
    }
  }
}
```

### PumpPortal Trading API

**URL**: https://pumpportal.fun

Features:
- Lightning Transaction API (<1 sec execution)
- WebSocket for real-time data
- Rate limits: 25 req/sec, 15 WS max
- No historical data access

### DefiLlama API

```
GET https://api.llama.fi/protocol/pump.fun
```
Returns: TVL, fees, revenue, volume history

### Moralis

Endpoints for pump.fun tokens:
- Token metadata
- OHLCV data
- Swap history
- Liquidity data
