# Data Analysis Results
*Generated from DefiLlama + pump.fun API data extraction*

## Ecosystem Metrics (from APIs)
```json
{
  "extraction_date": "2026-04-01 12:57:33 UTC",
  "data_sources": {
    "protocol_overview": "api.llama.fi/protocol/pump.fun (1554 bytes, SUCCESS)",
    "protocol_pump-fun": "api.llama.fi/protocol/pump-fun (NOT FOUND)",
    "protocol_pumpfun": "api.llama.fi/protocol/pumpfun (NOT FOUND)",
    "fees_pump_fun": "api.llama.fi/summary/fees/pump.fun (51KB, SUCCESS)",
    "fees_pumpswap": "api.llama.fi/summary/fees/pumpswap (28KB, SUCCESS)",
    "dexs_pumpswap": "api.llama.fi/summary/dexs/pumpswap (29KB, SUCCESS)",
    "overview_fees_solana": "api.llama.fi/overview/fees/solana (1.9MB, SUCCESS - filtered for pump)",
    "overview_dexs_solana": "api.llama.fi/overview/dexs/solana (758KB, SUCCESS - filtered for pump)",
    "fees_llama_fi": "fees.llama.fi/fees/pump.fun (FAILED - domain not resolving)"
  },
  "pump_fun_launchpad": {
    "protocol_info": {
      "id": "4449",
      "name": "pump.fun",
      "symbol": "PUMP",
      "chain": "Solana",
      "category": "Launchpad",
      "description": "Launch a coin that is instantly tradeable in one click for free",
      "url": "https://www.pump.fun/",
      "address": "solana:pumpCmXqMfrsAkQ5r49WcJnRayYRqmXz6ae8H7H9Dfn",
      "twitter": "Pumpfun",
      "gecko_id": "pump-fun",
      "listed_at_timestamp": 1712427917,
      "market_cap": 1010718085.279854,
      "parent_protocol": "parent#pump",
      "other_protocols_in_ecosystem": [
        "Pump",
        "PumpSwap",
        "pump.fun",
        "Padre"
      ],
      "raises": [
        {
          "date": 1752278400,
          "name": "pump.fun",
          "round": "Private token sale",
          "amount": 400,
          "chains": [],
          "sector": "Launch a coin that is instantly tradeable in one click",
          "category": null,
          "categoryGroup": null,
          "leadInvestors": [],
          "otherInvestors": [],
          "valuation": null,
          "defillamaId": "4449"
        },
        {
          "date": 1752278400,
          "name": "pump.fun",
          "round": "ICO",
          "amount": 600,
          "chains": [
            "Solana"
          ],
          "sector": "Launch a coin that is instantly tradeable in one click",
          "category": "DeFi",
          "categoryGroup": "DeFi & CeFi",
          "source": "https://x.com/Ashcryptoreal/status/1944038769126257028",
          "leadInvestors": [],
          "otherInvestors": [],
          "valuation": "4000",
          "defillamaId": "4449"
        }
      ]
    },
    "fees_and_revenue": {
      "total_fees_24h_usd": 757844,
      "total_fees_48h_to_24h_usd": 1130508,
      "total_fees_7d_usd": 4976672,
      "total_fees_30d_usd": 23605997,
      "total_fees_all_time_usd": 986269351,
      "change_1d_percent": -32.96,
      "methodology": {
        "Fees": "Trading and launching tokens fees paid by users",
        "Revenue": "Trading and launching tokens fees paid by users",
        "ProtocolRevenue": "pump.fun takes all fees paid by users",
        "HoldersRevenue": "PUMP token buybacks from the revenue"
      },
      "breakdown_methodology": {
        "Fees": {
          "LaunchpadFee": "Trade fees from launchpad"
        },
        "Revenue": {
          "LaunchpadFee": "Trade fees from launchpad that goes to the protocol"
        },
        "HoldersRevenue": {
          "Token Buy Back": "Pump token buyback"
        }
      },
      "data_points_count": 761
    },
    "fees_recent_daily": [
      {
        "timestamp": 1774396800,
        "date": "2026-03-25",
        "fees_usd": 791165
      },
      {
        "timestamp": 1774483200,
        "date": "2026-03-26",
        "fees_usd": 720354
      },
      {
        "timestamp": 1774569600,
        "date": "2026-03-27",
        "fees_usd": 705480
      },
      {
        "timestamp": 1774656000,
        "date": "2026-03-28",
        "fees_usd": 249039
      },
      {
        "timestamp": 1774742400,
        "date": "2026-03-29",
        "fees_usd": 622282
      },
      {
        "timestamp": 1774828800,
        "date": "2026-03-30",
        "fees_usd": 1130508
      },
      {
        "timestamp": 1774915200,
        "date": "2026-03-31",
        "fees_usd": 757844
      }
    ],
    "dex_volume": {
      "volume_24h_usd": 27270172,
      "volume_48h_to_24h_usd": 92200927,
      "volume_7d_usd": 370529453,
      "volume_30d_usd": 1703933470,
      "volume_all_time_usd": 87129081060,
      "volume_1y_usd": 33409296795,
      "change_1d_percent": -70.42,
      "change_7d_percent": -51.58,
      "change_1m_percent": -55.29
    }
  },
  "pumpswap_dex": {
    "dex_volume": {
      "volume_24h_usd": 92313417,
      "volume_48h_to_24h_usd": 84762673,
      "volume_7d_usd": 410000033,
      "volume_30d_usd": 1425045112,
      "volume_all_time_usd": 68883416452,
      "change_1d_percent": 8.91,
      "description": "The native dex for pump.fun",
      "data_points_count": 401
    },
    "volume_recent_daily": [
      {
        "timestamp": 1774396800,
        "date": "2026-03-25",
        "volume_usd": 56597809
      },
      {
        "timestamp": 1774483200,
        "date": "2026-03-26",
        "volume_usd": 46756660
      },
      {
        "timestamp": 1774569600,
        "date": "2026-03-27",
        "volume_usd": 46721132
      },
      {
        "timestamp": 1774656000,
        "date": "2026-03-28",
        "volume_usd": 42449780
      },
      {
        "timestamp": 1774742400,
        "date": "2026-03-29",
        "volume_usd": 40398562
      },
      {
        "timestamp": 1774828800,
        "date": "2026-03-30",
        "volume_usd": 84762673
      },
      {
        "timestamp": 1774915200,
        "date": "2026-03-31",
        "volume_usd": 92313417
      }
    ],
    "fees_and_revenue": {
      "total_fees_24h_usd": 1561839,
      "total_fees_48h_to_24h_usd": 1711041,
      "total_fees_7d_usd": 8738922,
      "total_fees_30d_usd": 44772038,
      "total_fees_all_time_usd": 545351804,
      "change_1d_percent": -8.72,
      "methodology": {
        "UserFees": "Swap fees paid by users",
        "Fees": "Total fees collected from all sources, including LP fees (0.20%) and protocol fees (0.05%) and coin creator fees (0.05%) from each trade",
        "Revenue": "Revenue kept by the protocol, which is the 0.05% protocol fee from each trade",
        "ProtocolRevenue": "Percentage of swap fees going to treasury",
        "HoldersRevenue": "Money going to governance token holders",
        "SupplySideRevenue": "Value earned by liquidity providers, which is the 0.20% LP fee from each trade",
        "Volume": "Tracks the trading volume across all pairs on PumpFun AMM"
      },
      "breakdown_methodology": {
        "Fees": {
          "ProtocolFees": "Trade fees from PumpFun AMM that goes to the protocol",
          "DexLPFees": "Trade fees from PumpFun AMM that goes to liquidity providers",
          "DexCreatorFees": "Trade fees from PumpFun AMM that goes to coin creators"
        },
        "Revenue": {
          "ProtocolFees": "Trade fees from PumpFun AMM that goes to the protocol"
        },
        "SupplySideRevenue": {
          "DexLPFees": "Trade fees from PumpFun AMM that goes to liquidity providers",
          "DexCreatorFees": "Trade fees from PumpFun AMM that goes to coin creators"
        }
      }
    }
  },
  "combined_pump_ecosystem": {
    "combined_fees_24h_usd": 2319683,
    "combined_fees_30d_usd": 68378035,
    "combined_fees_all_time_usd": 1531621155,
    "combined_volume_24h_usd": 119583589,
    "combined_volume_30d_usd": 3128978582,
    "combined_volume_all_time_usd": 156012497512,
    "market_cap_usd": 1010718085.279854,
    "components": [
      "pump.fun (Launchpad)",
      "PumpSwap (DEX)"
    ]
  }
}
```

## pump.fun Revenue Analysis (from DefiLlama)

| Metric | Value |
|--------|-------|
| Total Revenue (all time) | $986.3M |
| Peak Daily Revenue | $15.46M (2025-01-24) |
| Average Daily Revenue | $1296K |
| Last 30 Days Revenue | $23.6M |
| Data Points | 761 days |
| Date Range | 2024-03-01 to 2026-03-31 |

### Monthly Revenue Breakdown

| Month | Revenue |
|-------|--------|
| 2024-03 | $2.4M |
| 2024-04 | $10.5M |
| 2024-05 | $16.6M |
| 2024-06 | $20.8M |
| 2024-07 | $28.6M |
| 2024-08 | $20.5M |
| 2024-09 | $14.4M |
| 2024-10 | $30.5M |
| 2024-11 | $93.9M |
| 2024-12 | $82.9M |
| 2025-01 | $148.1M |
| 2025-02 | $74.6M |
| 2025-03 | $40.4M |
| 2025-04 | $49.6M |
| 2025-05 | $52.0M |
| 2025-06 | $40.6M |
| 2025-07 | $17.3M |
| 2025-08 | $41.1M |
| 2025-09 | $43.1M |
| 2025-10 | $28.5M |
| 2025-11 | $24.6M |
| 2025-12 | $23.5M |
| 2026-01 | $31.8M |
| 2026-02 | $25.6M |
| 2026-03 | $24.5M |

## PumpSwap Volume Analysis

| Metric | Value |
|--------|-------|
| Total Volume | $68.9B |
| Peak Daily Volume | $893M |
| Average Daily Volume | $172M |
| Last 30 Days Volume | $1.43B |

## Charts Generated

### Daily & Cumulative Revenue
![Daily & Cumulative Revenue](charts/revenue_over_time.png)

### Quarterly Revenue Breakdown
![Quarterly Revenue Breakdown](charts/quarterly_revenue.png)

### PumpSwap DEX Volume
![PumpSwap DEX Volume](charts/pumpswap_volume.png)

### Combined Ecosystem Fees
![Combined Ecosystem Fees](charts/combined_ecosystem_fees.png)

### Live Token Distribution
![Live Token Distribution](charts/live_token_analysis.png)

### Monthly Revenue Heatmap
![Monthly Revenue Heatmap](charts/monthly_revenue.png)

