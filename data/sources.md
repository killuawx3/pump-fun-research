# Data Sources Reference Guide

## Tier 1: Free, High-Quality

### DefiLlama
- **URL**: https://defillama.com/protocol/pump.fun
- **Data**: Fees, revenue, volume, quarterly income statements
- **Auth**: None required
- **Best for**: Revenue and volume trends

### Dune Analytics
- **URL**: https://dune.com/adam_tehc/pumpfun (best dashboard)
- **Data**: Token launches, graduation rates, revenue, wallet analysis
- **Auth**: Free account for viewing
- **Best for**: Custom SQL queries on pump.fun data

## Tier 2: Free with Limits

### Bitquery
- **URL**: https://docs.bitquery.io/docs/blockchain/Solana/PumpFun/
- **Data**: Real-time trades, new tokens, OHLCV, ATH, market cap
- **Auth**: API key required (free tier available)
- **Best for**: Real-time and historical token data

### Moralis
- **URL**: https://docs.moralis.com/get-started/tutorials/data-api/tokens-and-markets/get-pump-fun-tokens-swaps-and-prices
- **Data**: Liquidity, metadata, OHLCV, swaps
- **Auth**: API key required

### Token Terminal
- **URL**: https://tokenterminal.com/explorer/projects/pumpfun
- **Data**: 27+ metrics including DAU, WAU, MAU, revenue
- **Auth**: Free tier available

## Tier 3: On-Chain Direct

### Solana RPC
- **Program ID**: `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`
- **Methods**: getAccountInfo, getProgramAccounts, logsSubscribe
- **Best for**: Real-time bonding curve data, specific token lookups

### Helius
- **URL**: https://www.helius.dev
- **Data**: Yellowstone gRPC, enhanced transactions, DAS metadata
- **Best for**: Streaming pump AMM data

### Shyft
- **URL**: https://docs.shyft.to
- **Data**: Parsed PumpSwap pool data, Yellowstone gRPC
- **Best for**: Migration detection

## Tier 4: Unofficial APIs

### pump.fun Internal APIs
- **Documented by**: github.com/BankkRoll/pumpfun-apis
- **Endpoints**: 483 documented
- **Base URLs**:
  - Frontend API v3: `https://frontend-api-v3.pump.fun/`
  - Advanced Analytics v2: `https://advanced-api-v2.pump.fun/`
  - Profile API: `https://profile-api.pump.fun`
  - Swap API: `https://swap-api.pump.fun`
  - Volatility API: `https://volatility-api-v2.pump.fun`
  - Market API: `https://market-api.pump.fun`
  - Clips API: `https://clips-api.pump.fun`
- **Auth**: Most require JWT with Origin: https://pump.fun
- **Note**: Unofficial, may break without notice

### PumpPortal
- **URL**: https://pumpportal.fun
- **Data**: Lightning trading API (<1 sec), WebSocket
- **Limits**: 25 req/sec, max 15 WS connections
- **Note**: No historical data, no official token
