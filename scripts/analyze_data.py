#!/usr/bin/env python3
"""Analyze pump.fun extracted data and generate charts."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

DATA_DIR = Path(os.path.expanduser("~/pump-fun-research/data/extracted"))
CHARTS_DIR = Path(os.path.expanduser("~/pump-fun-research/analysis/charts"))
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

plt.style.use('dark_background')
COLORS = {
    'primary': '#FF6B35',  # pump.fun orange
    'secondary': '#00D4AA',  # teal
    'accent': '#FFD700',  # gold
    'red': '#FF4444',
    'blue': '#4488FF',
    'purple': '#AA44FF',
    'gray': '#888888',
}

def load_json(filename):
    path = DATA_DIR / filename
    if not path.exists():
        print(f"WARNING: {filename} not found")
        return None
    with open(path) as f:
        return json.load(f)


def chart1_revenue_over_time():
    """Daily and cumulative revenue from DefiLlama fees data."""
    data = load_json("summary-fees-pump-fun.json")
    if not data or "totalDataChart" not in data:
        print("No fee data available")
        return
    
    chart_data = data["totalDataChart"]
    dates = [datetime.fromtimestamp(d[0], tz=timezone.utc) for d in chart_data]
    daily_fees = [d[1] for d in chart_data]
    
    # Create pandas series for rolling averages
    df = pd.DataFrame({'date': dates, 'fees': daily_fees})
    df['rolling_7d'] = df['fees'].rolling(7).mean()
    df['rolling_30d'] = df['fees'].rolling(30).mean()
    df['cumulative'] = df['fees'].cumsum()
    
    # Plot 1: Daily Revenue + Rolling Averages
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), gridspec_kw={'height_ratios': [1.2, 1]})
    fig.suptitle('pump.fun Revenue Analysis', fontsize=18, fontweight='bold', color='white')
    
    ax1.bar(df['date'], df['fees'], alpha=0.3, color=COLORS['primary'], label='Daily Fees', width=1)
    ax1.plot(df['date'], df['rolling_7d'], color=COLORS['secondary'], linewidth=1.5, label='7-day MA')
    ax1.plot(df['date'], df['rolling_30d'], color=COLORS['accent'], linewidth=2, label='30-day MA')
    ax1.set_ylabel('Daily Fees (USD)', fontsize=12)
    ax1.set_title('Daily Revenue', fontsize=14)
    ax1.legend(fontsize=10)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
    ax1.grid(alpha=0.2)
    
    # Annotate peak
    peak_idx = df['fees'].idxmax()
    peak_date = df.loc[peak_idx, 'date']
    peak_val = df.loc[peak_idx, 'fees']
    ax1.annotate(f'Peak: ${peak_val/1e6:.1f}M', 
                xy=(peak_date, peak_val), xytext=(peak_date, peak_val*1.3),
                arrowprops=dict(arrowstyle='->', color='white'), fontsize=10, color='white',
                ha='center')
    
    # Plot 2: Cumulative Revenue
    ax2.fill_between(df['date'], 0, df['cumulative'], alpha=0.4, color=COLORS['primary'])
    ax2.plot(df['date'], df['cumulative'], color=COLORS['primary'], linewidth=2)
    ax2.set_ylabel('Cumulative Revenue (USD)', fontsize=12)
    ax2.set_title('Cumulative Revenue', fontsize=14)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.0f}M'))
    ax2.grid(alpha=0.2)
    
    # Mark $1B milestone
    billion_idx = df[df['cumulative'] >= 1e9].index
    if len(billion_idx) > 0:
        b_date = df.loc[billion_idx[0], 'date']
        ax2.axhline(y=1e9, color=COLORS['accent'], linestyle='--', alpha=0.5)
        ax2.annotate('$1 BILLION', xy=(b_date, 1e9), fontsize=12, color=COLORS['accent'],
                    fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'revenue_over_time.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Chart 1: Revenue over time")


def chart2_quarterly_revenue():
    """Quarterly revenue breakdown."""
    data = load_json("summary-fees-pump-fun.json")
    if not data or "totalDataChart" not in data:
        return
    
    chart_data = data["totalDataChart"]
    quarterly = defaultdict(float)
    
    for d in chart_data:
        dt = datetime.fromtimestamp(d[0], tz=timezone.utc)
        q = f"Q{(dt.month-1)//3 + 1} {dt.year}"
        quarterly[q] += d[1]
    
    quarters = list(quarterly.keys())
    revenues = list(quarterly.values())
    
    fig, ax = plt.subplots(figsize=(14, 7))
    bars = ax.bar(quarters, revenues, color=[COLORS['primary'] if r < max(revenues) else COLORS['accent'] for r in revenues],
                  edgecolor='white', linewidth=0.5)
    
    for bar, rev in zip(bars, revenues):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(revenues)*0.02,
               f'${rev/1e6:.0f}M', ha='center', fontsize=10, fontweight='bold', color='white')
    
    ax.set_title('pump.fun Quarterly Revenue', fontsize=16, fontweight='bold')
    ax.set_ylabel('Revenue (USD)', fontsize=12)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.0f}M'))
    ax.grid(axis='y', alpha=0.2)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'quarterly_revenue.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Chart 2: Quarterly revenue")


def chart3_pumpswap_volume():
    """PumpSwap DEX volume over time."""
    data = load_json("summary-dexs-pumpswap.json")
    if not data or "totalDataChart" not in data:
        print("No PumpSwap volume data")
        return
    
    chart_data = data["totalDataChart"]
    dates = [datetime.fromtimestamp(d[0], tz=timezone.utc) for d in chart_data]
    volumes = [d[1] for d in chart_data]
    
    df = pd.DataFrame({'date': dates, 'volume': volumes})
    df['rolling_7d'] = df['volume'].rolling(7).mean()
    df['cumulative'] = df['volume'].cumsum()
    
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.bar(df['date'], df['volume'], alpha=0.3, color=COLORS['blue'], width=1)
    ax.plot(df['date'], df['rolling_7d'], color=COLORS['secondary'], linewidth=2, label='7-day MA')
    ax.set_title('PumpSwap DEX Daily Volume', fontsize=16, fontweight='bold')
    ax.set_ylabel('Daily Volume (USD)', fontsize=12)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.0f}M'))
    ax.legend(fontsize=11)
    ax.grid(alpha=0.2)
    
    total = sum(volumes)
    ax.text(0.02, 0.95, f'Total Volume: ${total/1e9:.1f}B', transform=ax.transAxes,
           fontsize=13, fontweight='bold', color=COLORS['accent'], va='top')
    
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'pumpswap_volume.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Chart 3: PumpSwap volume")


def chart4_combined_ecosystem():
    """Combined pump.fun + PumpSwap fees."""
    pump_data = load_json("summary-fees-pump-fun.json")
    swap_data = load_json("summary-fees-pumpswap.json")
    
    if not pump_data or not swap_data:
        return
    
    # Merge by date
    pump_fees = {d[0]: d[1] for d in pump_data.get("totalDataChart", [])}
    swap_fees = {d[0]: d[1] for d in swap_data.get("totalDataChart", [])}
    
    all_dates = sorted(set(pump_fees.keys()) | set(swap_fees.keys()))
    dates = [datetime.fromtimestamp(d, tz=timezone.utc) for d in all_dates]
    p_vals = [pump_fees.get(d, 0) for d in all_dates]
    s_vals = [swap_fees.get(d, 0) for d in all_dates]
    
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.stackplot(dates, p_vals, s_vals, 
                labels=['pump.fun (Bonding Curve)', 'PumpSwap (DEX)'],
                colors=[COLORS['primary'], COLORS['blue']], alpha=0.7)
    
    ax.set_title('pump.fun Ecosystem — Combined Daily Fees', fontsize=16, fontweight='bold')
    ax.set_ylabel('Daily Fees (USD)', fontsize=12)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(alpha=0.2)
    
    total_pump = sum(p_vals)
    total_swap = sum(s_vals)
    ax.text(0.98, 0.95, f'pump.fun: ${total_pump/1e6:.0f}M\nPumpSwap: ${total_swap/1e6:.0f}M\nTotal: ${(total_pump+total_swap)/1e6:.0f}M',
           transform=ax.transAxes, fontsize=11, color='white', va='top', ha='right',
           bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'combined_ecosystem_fees.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Chart 4: Combined ecosystem fees")


def chart5_live_token_analysis():
    """Analyze the live token data from pump.fun APIs."""
    data = load_json("coins-graduated.json")
    if not data:
        data = load_json("coins-latest.json")
    if not data:
        print("No live token data")
        return
    
    coins = data if isinstance(data, list) else data.get("coins", data.get("data", []))
    if not coins:
        print("No coins found in data")
        return
    
    # Extract market caps and other metrics
    market_caps = []
    volumes = []
    holder_counts = []
    
    for coin in coins:
        mc = coin.get("marketCap") or coin.get("usd_market_cap") or coin.get("market_cap") or 0
        if isinstance(mc, (int, float)) and mc > 0:
            market_caps.append(mc)
        vol = coin.get("volume") or coin.get("volume_24h") or 0
        if isinstance(vol, (int, float)) and vol > 0:
            volumes.append(vol)
        holders = coin.get("numHolders") or coin.get("holder_count") or 0
        if isinstance(holders, (int, float)) and holders > 0:
            holder_counts.append(holders)
    
    if not market_caps:
        print("No market cap data found")
        return
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle(f'pump.fun Live Token Analysis (n={len(coins)} tokens)', fontsize=16, fontweight='bold')
    
    # Market cap distribution
    ax1 = axes[0]
    bins = [0, 1e4, 5e4, 1e5, 5e5, 1e6, 5e6, 1e7, 1e8, 1e9]
    labels = ['<$10K', '$10-50K', '$50-100K', '$100-500K', '$500K-1M', '$1-5M', '$5-10M', '$10-100M', '>$100M']
    counts, _ = np.histogram(market_caps, bins=bins)
    
    colors = [COLORS['red']] * 3 + [COLORS['primary']] * 3 + [COLORS['secondary']] * 2 + [COLORS['accent']]
    bars = ax1.barh(labels[:len(counts)], counts, color=colors[:len(counts)])
    ax1.set_title('Market Cap Distribution', fontsize=13)
    ax1.set_xlabel('Number of Tokens')
    for bar, count in zip(bars, counts):
        if count > 0:
            ax1.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                   str(count), va='center', fontsize=10, color='white')
    
    # Top tokens by market cap
    ax2 = axes[1]
    sorted_coins = sorted(coins, key=lambda c: c.get("marketCap", 0) or c.get("usd_market_cap", 0) or 0, reverse=True)[:15]
    names = [c.get("ticker", c.get("symbol", c.get("name", "?")))[:10] for c in sorted_coins]
    mcaps = [(c.get("marketCap") or c.get("usd_market_cap", 0) or 0) for c in sorted_coins]
    
    bars = ax2.barh(range(len(names)), mcaps, color=COLORS['secondary'])
    ax2.set_yticks(range(len(names)))
    ax2.set_yticklabels(names, fontsize=9)
    ax2.set_title('Top 15 Tokens by Market Cap', fontsize=13)
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M' if x >= 1e6 else f'${x/1e3:.0f}K'))
    ax2.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'live_token_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Chart 5: Live token analysis ({len(coins)} tokens)")


def chart6_monthly_revenue_heatmap():
    """Monthly revenue heatmap."""
    data = load_json("summary-fees-pump-fun.json")
    if not data or "totalDataChart" not in data:
        return
    
    chart_data = data["totalDataChart"]
    monthly = defaultdict(float)
    
    for d in chart_data:
        dt = datetime.fromtimestamp(d[0], tz=timezone.utc)
        key = dt.strftime("%Y-%m")
        monthly[key] += d[1]
    
    months = sorted(monthly.keys())
    values = [monthly[m] for m in months]
    labels = [datetime.strptime(m, "%Y-%m").strftime("%b %y") for m in months]
    
    fig, ax = plt.subplots(figsize=(16, 5))
    
    # Create color gradient
    norm = plt.Normalize(min(values), max(values))
    cmap = plt.cm.YlOrRd
    colors = [cmap(norm(v)) for v in values]
    
    bars = ax.bar(labels, values, color=colors, edgecolor='white', linewidth=0.3)
    
    for bar, val in zip(bars, values):
        if val > max(values) * 0.15:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.02,
                   f'${val/1e6:.0f}M', ha='center', fontsize=8, rotation=45, color='white')
    
    ax.set_title('pump.fun Monthly Revenue', fontsize=16, fontweight='bold')
    ax.set_ylabel('Revenue (USD)')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.0f}M'))
    ax.grid(axis='y', alpha=0.2)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'monthly_revenue.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Chart 6: Monthly revenue")


def generate_analysis_summary():
    """Generate a markdown summary of the data analysis."""
    
    # Load summary data
    summary = load_json("pump-fun-summary.json")
    pump_fees = load_json("summary-fees-pump-fun.json")
    swap_fees = load_json("summary-fees-pumpswap.json")
    swap_vol = load_json("summary-dexs-pumpswap.json")
    
    lines = ["# Data Analysis Results\n"]
    lines.append("*Generated from DefiLlama + pump.fun API data extraction*\n\n")
    
    if summary:
        lines.append("## Ecosystem Metrics (from APIs)\n")
        lines.append("```json\n")
        lines.append(json.dumps(summary, indent=2))
        lines.append("\n```\n\n")
    
    # Revenue stats from raw data
    if pump_fees and "totalDataChart" in pump_fees:
        chart_data = pump_fees["totalDataChart"]
        daily_fees = [d[1] for d in chart_data]
        total = sum(daily_fees)
        peak = max(daily_fees)
        peak_date = datetime.fromtimestamp(chart_data[daily_fees.index(peak)][0], tz=timezone.utc)
        avg = total / len(daily_fees)
        recent_30d = sum(daily_fees[-30:])
        
        lines.append("## pump.fun Revenue Analysis (from DefiLlama)\n\n")
        lines.append(f"| Metric | Value |\n|--------|-------|\n")
        lines.append(f"| Total Revenue (all time) | ${total/1e6:.1f}M |\n")
        lines.append(f"| Peak Daily Revenue | ${peak/1e6:.2f}M ({peak_date.strftime('%Y-%m-%d')}) |\n")
        lines.append(f"| Average Daily Revenue | ${avg/1e3:.0f}K |\n")
        lines.append(f"| Last 30 Days Revenue | ${recent_30d/1e6:.1f}M |\n")
        lines.append(f"| Data Points | {len(daily_fees)} days |\n")
        lines.append(f"| Date Range | {datetime.fromtimestamp(chart_data[0][0], tz=timezone.utc).strftime('%Y-%m-%d')} to {datetime.fromtimestamp(chart_data[-1][0], tz=timezone.utc).strftime('%Y-%m-%d')} |\n\n")
        
        # Monthly breakdown
        monthly = defaultdict(float)
        for d in chart_data:
            dt = datetime.fromtimestamp(d[0], tz=timezone.utc)
            monthly[dt.strftime("%Y-%m")] += d[1]
        
        lines.append("### Monthly Revenue Breakdown\n\n")
        lines.append("| Month | Revenue |\n|-------|--------|\n")
        for m in sorted(monthly.keys()):
            lines.append(f"| {m} | ${monthly[m]/1e6:.1f}M |\n")
        lines.append("\n")
    
    if swap_vol and "totalDataChart" in swap_vol:
        chart_data = swap_vol["totalDataChart"]
        daily_vol = [d[1] for d in chart_data]
        total_vol = sum(daily_vol)
        lines.append("## PumpSwap Volume Analysis\n\n")
        lines.append(f"| Metric | Value |\n|--------|-------|\n")
        lines.append(f"| Total Volume | ${total_vol/1e9:.1f}B |\n")
        lines.append(f"| Peak Daily Volume | ${max(daily_vol)/1e6:.0f}M |\n")
        lines.append(f"| Average Daily Volume | ${(total_vol/len(daily_vol))/1e6:.0f}M |\n")
        lines.append(f"| Last 30 Days Volume | ${sum(daily_vol[-30:])/1e9:.2f}B |\n\n")
    
    lines.append("## Charts Generated\n\n")
    charts = [
        ("revenue_over_time.png", "Daily & Cumulative Revenue"),
        ("quarterly_revenue.png", "Quarterly Revenue Breakdown"),
        ("pumpswap_volume.png", "PumpSwap DEX Volume"),
        ("combined_ecosystem_fees.png", "Combined Ecosystem Fees"),
        ("live_token_analysis.png", "Live Token Distribution"),
        ("monthly_revenue.png", "Monthly Revenue Heatmap"),
    ]
    for fname, title in charts:
        lines.append(f"### {title}\n![{title}](charts/{fname})\n\n")
    
    output = "".join(lines)
    output_path = Path(os.path.expanduser("~/pump-fun-research/analysis/data-analysis-results.md"))
    output_path.write_text(output)
    print(f"✓ Analysis summary written to {output_path}")


if __name__ == "__main__":
    print("=" * 60)
    print("pump.fun Data Analysis & Chart Generation")
    print("=" * 60)
    print()
    chart1_revenue_over_time()
    chart2_quarterly_revenue()
    chart3_pumpswap_volume()
    chart4_combined_ecosystem()
    chart5_live_token_analysis()
    chart6_monthly_revenue_heatmap()
    print()
    generate_analysis_summary()
    print()
    print("Done! Charts saved to:", CHARTS_DIR)
