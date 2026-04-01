import json
import os

os.chdir(os.path.expanduser('~/pump-fun-research/data/extracted'))

# 1. Protocol overview (pump.fun)
print('='*60)
print('=== protocol-pump.fun.json ===')
with open('protocol-pump.fun.json') as f:
    d = json.load(f)
for k in d:
    if isinstance(d[k], (str, int, float, bool, type(None))):
        print(f'  {k}: {d[k]}')
    elif isinstance(d[k], list) and len(d[k]) < 5:
        print(f'  {k}: {d[k]}')
    elif isinstance(d[k], dict):
        print(f'  {k}: {json.dumps(d[k])[:200]}')
    else:
        print(f'  {k}: [{type(d[k]).__name__}, len={len(d[k]) if hasattr(d[k],"__len__") else "?"}]')

# 2. summary-fees-pump-fun.json (the one that worked with pump.fun slug)
print('\n' + '='*60)
print('=== summary-fees-pump-fun.json (fees/revenue) ===')
with open('summary-fees-pump-fun.json') as f:
    d = json.load(f)
# Print top-level non-chart fields
for k in d:
    if k in ('totalDataChart', 'totalDataChartBreakdown'):
        arr = d[k]
        if arr:
            print(f'  {k}: {len(arr)} entries, latest: {arr[-1]}')
    elif isinstance(d[k], (str, int, float, bool, type(None))):
        print(f'  {k}: {d[k]}')
    elif isinstance(d[k], list) and len(d[k]) < 5:
        print(f'  {k}: {d[k]}')
    elif isinstance(d[k], dict):
        print(f'  {k}: {json.dumps(d[k])[:300]}')
    else:
        print(f'  {k}: [{type(d[k]).__name__}, len={len(d[k]) if hasattr(d[k],"__len__") else "?"}]')

# 3. summary-dexs-pumpswap.json 
print('\n' + '='*60)
print('=== summary-dexs-pumpswap.json (PumpSwap DEX volume) ===')
with open('summary-dexs-pumpswap.json') as f:
    d = json.load(f)
for k in d:
    if k in ('totalDataChart', 'totalDataChartBreakdown'):
        arr = d[k]
        if arr:
            print(f'  {k}: {len(arr)} entries, latest: {arr[-1]}')
    elif isinstance(d[k], (str, int, float, bool, type(None))):
        print(f'  {k}: {d[k]}')
    elif isinstance(d[k], list) and len(d[k]) < 5:
        print(f'  {k}: {d[k]}')
    elif isinstance(d[k], dict):
        print(f'  {k}: {json.dumps(d[k])[:300]}')
    else:
        print(f'  {k}: [{type(d[k]).__name__}, len={len(d[k]) if hasattr(d[k],"__len__") else "?"}]')

# 4. summary-fees-pumpswap.json
print('\n' + '='*60)
print('=== summary-fees-pumpswap.json (PumpSwap fees) ===')
with open('summary-fees-pumpswap.json') as f:
    d = json.load(f)
for k in d:
    if k in ('totalDataChart', 'totalDataChartBreakdown'):
        arr = d[k]
        if arr:
            print(f'  {k}: {len(arr)} entries, latest: {arr[-1]}')
    elif isinstance(d[k], (str, int, float, bool, type(None))):
        print(f'  {k}: {d[k]}')
    elif isinstance(d[k], list) and len(d[k]) < 5:
        print(f'  {k}: {d[k]}')
    elif isinstance(d[k], dict):
        print(f'  {k}: {json.dumps(d[k])[:300]}')
    else:
        print(f'  {k}: [{type(d[k]).__name__}, len={len(d[k]) if hasattr(d[k],"__len__") else "?"}]')

# 5. Filter pump.fun from Solana fees overview
print('\n' + '='*60)
print('=== overview-fees-solana.json (filtering for pump) ===')
with open('overview-fees-solana.json') as f:
    d = json.load(f)
if 'protocols' in d:
    for p in d['protocols']:
        name = p.get('name', '').lower()
        if 'pump' in name:
            print(f"\n  Protocol: {p.get('name')}")
            for k, v in p.items():
                if isinstance(v, (str, int, float, bool, type(None))):
                    print(f'    {k}: {v}')
                elif isinstance(v, dict):
                    print(f'    {k}: {json.dumps(v)[:200]}')

# 6. Filter pump from Solana DEX overview
print('\n' + '='*60)
print('=== overview-dexs-solana.json (filtering for pump) ===')
with open('overview-dexs-solana.json') as f:
    d = json.load(f)
if 'protocols' in d:
    for p in d['protocols']:
        name = p.get('name', '').lower()
        if 'pump' in name:
            print(f"\n  Protocol: {p.get('name')}")
            for k, v in p.items():
                if isinstance(v, (str, int, float, bool, type(None))):
                    print(f'    {k}: {v}')
                elif isinstance(v, dict):
                    print(f'    {k}: {json.dumps(v)[:200]}')
