import json
import os
from datetime import datetime

os.chdir(os.path.expanduser('~/pump-fun-research/data/extracted'))

summary = {
    "extraction_date": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
    "data_sources": {},
    "pump_fun_launchpad": {},
    "pumpswap_dex": {},
    "combined_pump_ecosystem": {}
}

# --- pump.fun Launchpad Protocol Overview ---
with open('protocol-pump.fun.json') as f:
    proto = json.load(f)
summary["pump_fun_launchpad"]["protocol_info"] = {
    "id": proto.get("id"),
    "name": proto.get("name"),
    "symbol": proto.get("symbol"),
    "chain": proto.get("chain"),
    "category": proto.get("category"),
    "description": proto.get("description"),
    "url": proto.get("url"),
    "address": proto.get("address"),
    "twitter": proto.get("twitter"),
    "gecko_id": proto.get("gecko_id"),
    "listed_at_timestamp": proto.get("listedAt"),
    "market_cap": proto.get("mcap"),
    "parent_protocol": proto.get("parentProtocol"),
    "other_protocols_in_ecosystem": proto.get("otherProtocols"),
    "raises": proto.get("raises"),
}

# --- pump.fun Fees/Revenue ---
with open('summary-fees-pump-fun.json') as f:
    fees = json.load(f)
summary["pump_fun_launchpad"]["fees_and_revenue"] = {
    "total_fees_24h_usd": fees.get("total24h"),
    "total_fees_48h_to_24h_usd": fees.get("total48hto24h"),
    "total_fees_7d_usd": fees.get("total7d"),
    "total_fees_30d_usd": fees.get("total30d"),
    "total_fees_all_time_usd": fees.get("totalAllTime"),
    "change_1d_percent": fees.get("change_1d"),
    "methodology": fees.get("methodology"),
    "breakdown_methodology": fees.get("breakdownMethodology"),
    "data_points_count": len(fees.get("totalDataChart", [])),
}

# Latest 5 fee data points
chart = fees.get("totalDataChart", [])
if chart:
    summary["pump_fun_launchpad"]["fees_recent_daily"] = [
        {"timestamp": ts, "date": datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d"), "fees_usd": val}
        for ts, val in chart[-7:]
    ]

# --- pump.fun DEX Volume ---
with open('overview-dexs-solana.json') as f:
    dexs = json.load(f)
for p in dexs.get('protocols', []):
    if p.get('name') == 'pump.fun':
        summary["pump_fun_launchpad"]["dex_volume"] = {
            "volume_24h_usd": p.get("total24h"),
            "volume_48h_to_24h_usd": p.get("total48hto24h"),
            "volume_7d_usd": p.get("total7d"),
            "volume_30d_usd": p.get("total30d"),
            "volume_all_time_usd": p.get("totalAllTime"),
            "volume_1y_usd": p.get("total1y"),
            "change_1d_percent": p.get("change_1d"),
            "change_7d_percent": p.get("change_7d"),
            "change_1m_percent": p.get("change_1m"),
        }
        break

# --- PumpSwap DEX Volume ---
with open('summary-dexs-pumpswap.json') as f:
    psdex = json.load(f)
summary["pumpswap_dex"]["dex_volume"] = {
    "volume_24h_usd": psdex.get("total24h"),
    "volume_48h_to_24h_usd": psdex.get("total48hto24h"),
    "volume_7d_usd": psdex.get("total7d"),
    "volume_30d_usd": psdex.get("total30d"),
    "volume_all_time_usd": psdex.get("totalAllTime"),
    "change_1d_percent": psdex.get("change_1d"),
    "description": psdex.get("description"),
    "data_points_count": len(psdex.get("totalDataChart", [])),
}

# PumpSwap recent daily volume
chart = psdex.get("totalDataChart", [])
if chart:
    summary["pumpswap_dex"]["volume_recent_daily"] = [
        {"timestamp": ts, "date": datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d"), "volume_usd": val}
        for ts, val in chart[-7:]
    ]

# --- PumpSwap Fees ---
with open('summary-fees-pumpswap.json') as f:
    psfees = json.load(f)
summary["pumpswap_dex"]["fees_and_revenue"] = {
    "total_fees_24h_usd": psfees.get("total24h"),
    "total_fees_48h_to_24h_usd": psfees.get("total48hto24h"),
    "total_fees_7d_usd": psfees.get("total7d"),
    "total_fees_30d_usd": psfees.get("total30d"),
    "total_fees_all_time_usd": psfees.get("totalAllTime"),
    "change_1d_percent": psfees.get("change_1d"),
    "methodology": psfees.get("methodology"),
    "breakdown_methodology": psfees.get("breakdownMethodology"),
}

# --- Combined Ecosystem Metrics ---
pf_fees_24h = fees.get("total24h", 0) or 0
ps_fees_24h = psfees.get("total24h", 0) or 0
pf_vol_24h = summary.get("pump_fun_launchpad", {}).get("dex_volume", {}).get("volume_24h_usd", 0) or 0
ps_vol_24h = psdex.get("total24h", 0) or 0

pf_fees_30d = fees.get("total30d", 0) or 0
ps_fees_30d = psfees.get("total30d", 0) or 0
pf_vol_30d = summary.get("pump_fun_launchpad", {}).get("dex_volume", {}).get("volume_30d_usd", 0) or 0
ps_vol_30d = psdex.get("total30d", 0) or 0

pf_fees_all = fees.get("totalAllTime", 0) or 0
ps_fees_all = psfees.get("totalAllTime", 0) or 0
pf_vol_all = summary.get("pump_fun_launchpad", {}).get("dex_volume", {}).get("volume_all_time_usd", 0) or 0
ps_vol_all = psdex.get("totalAllTime", 0) or 0

summary["combined_pump_ecosystem"] = {
    "combined_fees_24h_usd": pf_fees_24h + ps_fees_24h,
    "combined_fees_30d_usd": pf_fees_30d + ps_fees_30d,
    "combined_fees_all_time_usd": pf_fees_all + ps_fees_all,
    "combined_volume_24h_usd": pf_vol_24h + ps_vol_24h,
    "combined_volume_30d_usd": pf_vol_30d + ps_vol_30d,
    "combined_volume_all_time_usd": pf_vol_all + ps_vol_all,
    "market_cap_usd": proto.get("mcap"),
    "components": ["pump.fun (Launchpad)", "PumpSwap (DEX)"],
}

# Track data sources
summary["data_sources"] = {
    "protocol_overview": "api.llama.fi/protocol/pump.fun (1554 bytes, SUCCESS)",
    "protocol_pump-fun": "api.llama.fi/protocol/pump-fun (NOT FOUND)",
    "protocol_pumpfun": "api.llama.fi/protocol/pumpfun (NOT FOUND)",
    "fees_pump_fun": "api.llama.fi/summary/fees/pump.fun (51KB, SUCCESS)",
    "fees_pumpswap": "api.llama.fi/summary/fees/pumpswap (28KB, SUCCESS)",
    "dexs_pumpswap": "api.llama.fi/summary/dexs/pumpswap (29KB, SUCCESS)",
    "overview_fees_solana": "api.llama.fi/overview/fees/solana (1.9MB, SUCCESS - filtered for pump)",
    "overview_dexs_solana": "api.llama.fi/overview/dexs/solana (758KB, SUCCESS - filtered for pump)",
    "fees_llama_fi": "fees.llama.fi/fees/pump.fun (FAILED - domain not resolving)",
}

with open('pump-fun-summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print("Summary saved to pump-fun-summary.json")
print(f"File size: {os.path.getsize('pump-fun-summary.json')} bytes")

# Print key metrics
print("\n" + "="*60)
print("KEY METRICS SUMMARY")
print("="*60)
print(f"\n--- pump.fun Launchpad ---")
print(f"  Fees 24h:       ${pf_fees_24h:,.0f}")
print(f"  Fees 7d:        ${fees.get('total7d', 0):,.0f}")
print(f"  Fees 30d:       ${pf_fees_30d:,.0f}")
print(f"  Fees All Time:  ${pf_fees_all:,.0f}")
print(f"  Volume 24h:     ${pf_vol_24h:,.0f}")
print(f"  Volume 30d:     ${pf_vol_30d:,.0f}")
print(f"  Volume All Time:${pf_vol_all:,.0f}")

print(f"\n--- PumpSwap DEX ---")
print(f"  Fees 24h:       ${ps_fees_24h:,.0f}")
print(f"  Fees 7d:        ${psfees.get('total7d', 0):,.0f}")
print(f"  Fees 30d:       ${ps_fees_30d:,.0f}")
print(f"  Fees All Time:  ${ps_fees_all:,.0f}")
print(f"  Volume 24h:     ${ps_vol_24h:,.0f}")
print(f"  Volume 30d:     ${ps_vol_30d:,.0f}")
print(f"  Volume All Time:${ps_vol_all:,.0f}")

print(f"\n--- Combined Pump Ecosystem ---")
print(f"  Total Fees 24h:       ${pf_fees_24h + ps_fees_24h:,.0f}")
print(f"  Total Fees 30d:       ${pf_fees_30d + ps_fees_30d:,.0f}")
print(f"  Total Fees All Time:  ${pf_fees_all + ps_fees_all:,.0f}")
print(f"  Total Volume 24h:     ${pf_vol_24h + ps_vol_24h:,.0f}")
print(f"  Total Volume 30d:     ${pf_vol_30d + ps_vol_30d:,.0f}")
print(f"  Total Volume All Time:${pf_vol_all + ps_vol_all:,.0f}")
print(f"  Market Cap (PUMP):    ${proto.get('mcap', 0):,.0f}")
