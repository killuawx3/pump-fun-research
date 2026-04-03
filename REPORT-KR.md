# Pump.fun 러그풀 신호 탐지 — 연구 보고서

**날짜:** 2026년 4월 3일
**데이터 출처:** Dune Analytics — `pumpdotfun_solana.*` 디코딩 테이블, `dune.bumaye17.result_clean_pump_fun`
**샘플:** 2025년 1월 5일에 출시된 토큰 47,247개
**분류:** RUG 토큰 163개, HEALTHY 토큰 45개 (시가총액 궤적 기반 자체 라벨링)

---

## 1. Pump.fun 생태계 현황

단 하루(2025년 1월 5일) 동안 pump.fun에서 **47,247개의 토큰**이 출시되었습니다. 분류별 분포는 다음과 같습니다:

| 카테고리 | 수량 | % | 설명 |
|----------|------:|----:|------|
| 즉시 사망 | 19,962 | 42.3% | 시가총액이 $7K를 넘지 못함 |
| 낮은 관심 | 23,088 | 48.9% | 최대 시가총액 $7K–$20K |
| 중간 관심 | 3,576 | 7.6% | 최대 시가총액 $20K–$100K |
| 높은 관심 | 428 | 0.9% | 최대 시가총액 $100K–$1M |
| $1M 이상 | 92 | 0.2% | 시가총액 $1M+ 달성 |

**91.2%의 토큰이 시가총액 $20K를 넘지 못합니다.** 단 0.2%(92개 토큰)만이 $1M 이상에 도달했습니다.

> 출처: `SELECT COUNT(*), COUNT(CASE WHEN max_mcap < 7000 ...) FROM dune.bumaye17.result_clean_pump_fun`

![Pump.fun 토큰 결과 분포](charts/pumpfun_landscape.png)

### 주요 통계 (전체 데이터셋, 47,247 토큰)
- 최대 시가총액 중앙값: **$7,210**
- 시가총액 99번째 백분위수: **$116,700**
- 처음 10초 내 매수 거래량 중앙값: **2.61 SOL**
- 평균 첫 매수 횟수: **2.18명의 매수자**

---

## 2. 자체 라벨링 방법론

Pump.fun 러그풀에 대한 사전 구축된 라벨링 데이터셋이 존재하지 않기 때문에, **시가총액 궤적 분석**을 사용하여 자체적으로 구축했습니다.

### 라벨링 기준

**RUG** (n=163): 토큰이 처음 10분 이내에 정점을 찍고 (`max_mcap_10m > 80% of max_mcap`) 1시간 이내에 폭락 (`mcap_1h < 20% of max_mcap`). 이것은 펌프 앤 덤프 패턴으로 — 빠른 정점 후 즉각적인 폭락입니다.

**HEALTHY** (n=45): 토큰이 1시간 시점에도 여전히 성장 (`mcap_1h > 80% of mcap_10m`) 중이며 4시간 시점에서도 가치를 유지 (`mcap_4h > 20% of max_mcap`). 이것은 유기적 성장 패턴으로 — 점진적인 가격 상승입니다.

**적용 필터:** `max_mcap > $20,000`인 토큰만 포함 (의미 있는 분석을 위해 충분한 거래량이 있는 토큰).

> 출처: `SELECT account_mint, symbol, mcap_first_buy, mcap_10m, mcap_1h, mcap_4h, mcap_12h, last_mcap, max_mcap, max_mcap_10m, first_buy_cnt, first_buy_vol_sol, buy_sol_vol_10s, sell_vol_sol_1m FROM dune.bumaye17.result_clean_pump_fun WHERE max_mcap > 10000 ORDER BY max_mcap DESC LIMIT 500`

---

## 3. 특징 비교: RUG vs HEALTHY

### 3.1 전체 통계 비교 표

| 특징 | 분류 | 중앙값 | 평균 | P25 | P75 | 최소 | 최대 |
|------|------|-------:|-----:|----:|----:|----:|----:|
| **10초 내 매수량 (SOL)** | RUG | **34.41** | 43.15 | 7.70 | 85.01 | 0.15 | 141.95 |
| | HEALTHY | **5.09** | 22.18 | 2.47 | 29.26 | 0.68 | 135.30 |
| | **비율** | **6.8x** | | | | | |
| **첫 매수 횟수** | RUG | **2** | 4.50 | 1 | 4 | 1 | 27 |
| | HEALTHY | **2** | 3.07 | 1 | 3 | 1 | 23 |
| | **비율** | **1.0x** | | | | | |
| **첫 매수 거래량 (SOL)** | RUG | **4.24** | 17.00 | 2.21 | 17.56 | 0.10 | 160.17 |
| | HEALTHY | **3.26** | 10.89 | 1.70 | 6.30 | 0.02 | 85.01 |
| | **비율** | **1.3x** | | | | | |
| **1분 내 매도량 (SOL)** | RUG | **19.74** | 31.97 | 5.71 | 46.25 | 0.00 | 171.29 |
| | HEALTHY | **2.79** | 14.05 | 1.75 | 13.30 | 0.00 | 153.87 |
| | **비율** | **7.1x** | | | | | |
| **매도/매수 비율 (1분)** | RUG | **2.51** | 11.82 | | | | |
| | HEALTHY | **0.84** | 4.49 | | | | |
| | **비율** | **3.0x** | | | | | |
| **1시간 후 유지율 (%)** | RUG | **2.8%** | 4.0% | | | | |
| | HEALTHY | **19.3%** | 25.0% | | | | |
| | **비율** | **6.9x** | | | | | |
| **10분 시점 시가총액 성장** | RUG | **1.05x** | 8.78x | | | | |
| | HEALTHY | **2.12x** | 66.64x | | | | |
| | **비율** | **0.5x** | | | | | |

> 출처: `dune.bumaye17.result_clean_pump_fun` 필드에서 특징 추출: `buy_sol_vol_10s`, `first_buy_cnt`, `first_buy_vol_sol`, `sell_vol_sol_1m`, `mcap_first_buy`, `mcap_10m`, `mcap_1h`, `max_mcap`

![특징 분포](charts/rug_vs_healthy_features.png)
![신호 강도](charts/signal_strength.png)

---

## 4. 주요 발견 — 가장 강력한 신호들

### 신호 1: 처음 10초 내 매수 거래량 (6.8배 차이)

이것이 **가장 강력한 초기 신호**입니다. RUG 토큰은 처음 10초 이내에 중앙값 **34.41 SOL** ($7,000+)이 쏟아지는 반면, HEALTHY 토큰은 **5.09 SOL**에 불과합니다. 이는 펌프를 선점하는 조직적인 봇/스나이퍼 활동을 시사합니다.

**제안 임계값:** `buy_sol_vol_10s > 50 SOL` → 고위험

### 신호 2: 처음 1분 내 매도 거래량 (7.1배 차이)

RUG 토큰은 첫 1분 이내에 **19.74 SOL**의 매도 거래량을 보이며, HEALTHY 토큰은 **2.79 SOL**에 불과합니다. 내부자들이 출시 후 60초 이내에 이미 수익을 실현하고 있습니다.

**제안 임계값:** `sell_vol_sol_1m > 15 SOL` → 고위험

### 신호 3: 처음 1분 매도/매수 비율 (3.0배 차이)

RUG 토큰의 경우 첫 1분 동안 매도가 매수를 **2.51배** 초과합니다. HEALTHY 토큰은 **0.84배**로 더 균형 잡힌 비율을 보입니다 (여전히 순매수 상태). 이는 러그풀의 경우 누군가가 초기 매수 압력에 공격적으로 매도하고 있음을 의미합니다.

**제안 임계값:** `sell_buy_ratio > 2.0` → 고위험

### 신호 4: 1시간 후 가격 유지율 (6.9배 차이)

1시간 시점에서 RUG 토큰은 최고 시가총액의 **2.8%**만 유지하는 반면, HEALTHY 토큰은 **19.3%**를 유지합니다. 이것은 확인 신호(조기 경고가 아님)이지만 패턴을 검증하는 데 유효합니다.

### 신호 5: 10분 시점 시가총액 성장률 (2배 차이)

RUG 토큰은 10분 시점에 이미 정점을 찍었습니다 (1.05배 성장 = 첫 매수 이후 횡보/하락). HEALTHY 토큰은 10분 시점에서 **2.12배**로 여전히 성장 중입니다. 10분 체크포인트에서 토큰 가격이 **성장하지 않는다면**, 이미 정점을 찍고 곧 덤프될 가능성이 높습니다.

**제안 임계값:** `mcap_10m / mcap_first_buy < 1.2` → 경고

### 신호 6: 첫 매수 횟수 (가장 약한 신호, 1.0배)

첫 번째 트랜잭션 블록의 매수자 수는 그 자체로 강력한 구분 기준이 되지 않습니다 (두 분류 모두 중앙값 2). 하지만 꼬리 분포가 중요합니다 — RUG 토큰은 더 높은 분산을 보이며 (극단적인 경우 첫 블록 매수자가 최대 27명 vs HEALTHY는 23명), 이는 극단적 상황에서 봇 군집 활동을 시사합니다.

---

## 5. 거래별 사례 연구

### 사례 연구 A: $ASC (RUG)
- **최대 시가총액:** $5,239,791
- **1시간 시점 시가총액:** $427,234 (92% 하락)
- **10초 내 매수 거래량:** 96.0 SOL
- **1분 내 매도 거래량:** 11.0 SOL

`pumpdotfun_solana.pump_evt_tradeevent`에서 추출:
```
21:52:33 | BUY  | 1.563 SOL | user: 6E8syMcyc... (생성자 초기 매수)
21:52:34 | BUY  | 4.754 SOL | user: BNHsrnuv7... (스나이퍼 봇)
21:52:34 | SELL | 10.978 SOL | user: EqcwZCrWL... (즉시 매도 - 샌드위치)
21:52:34 | BUY  | 2.848 SOL | user: EqcwZCrWL... (동일 사용자가 더 싼 가격에 재매수)
21:52:34 | BUY  | 7.928 SOL | user: BQALoPHJn... (스나이퍼 봇)
21:52:34 | BUY  | 5.121 SOL | user: EXuo1rrME... (스나이퍼 봇)
21:52:34 | BUY  | 5.363 SOL | user: 3iavFiD8h... (스나이퍼 봇)
21:52:34 | BUY  | 4.950 SOL | user: 91AhAK1Gq... (스나이퍼 봇)
... 생성 후 1초 이내에 20개 이상의 지갑이 매수
```

**패턴:** 1초 이내에 대규모 봇 군집 매수. 한 사용자 (`EqcwZCrWL...`)가 같은 초 안에 매도와 재매수를 실행 — 전형적인 샌드위치 공격. Virtual SOL 준비금이 1초 만에 31 → 75 SOL로 급등합니다.

### 사례 연구 B: $HTERM (HEALTHY)
- **최대 시가총액:** $43,943,160
- **1시간 시점 시가총액:** $20,341,560 (최고점의 46% — 여전히 건전)
- **10초 내 매수 거래량:** 6.3 SOL
- **1분 내 매도 거래량:** 0.6 SOL

`pumpdotfun_solana.pump_evt_tradeevent`에서 추출:
```
18:06:28 | BUY  | 4.875 SOL | user: 6hSdkkY1D... (생성자 소량 매수)
18:06:28 | BUY  | 0.528 SOL | user: ZDLFG5UNP... (소규모 유기적 매수)
18:06:33 | BUY  | 0.502 SOL | user: 8W9Nv8T1b... (5초 후)
18:06:35 | BUY  | 0.267 SOL | user: 94yinPSx1... (유기적 유입)
18:06:44 | SELL | 0.512 SOL | user: 8W9Nv8T1b... (소규모 차익 실현, 정상)
18:07:58 | BUY  | 0.980 SOL | user: B6crdsm8b... (1.5분 후, 유기적)
18:08:47 | BUY  | 4.554 SOL | user: BShijgmzV... (2분 후, 대량 매수)
... 수 분에 걸쳐 점진적 축적
```

**패턴:** 정상적인 유기적 발견. 소규모 매수가 초 단위가 아닌 분 단위로 천천히 유입됩니다. Virtual SOL 준비금이 점진적으로 성장: 2분 이상에 걸쳐 30 → 35 → 46 SOL. 샌드위치 공격이나 봇 군집 없음.

![거래별 비교](charts/trade_by_trade_comparison.png)

---

## 6. 시가총액 궤적 패턴

가장 시각적으로 두드러지는 차이는 시가총액 궤적의 형태입니다.

### RUG 패턴: "스파이크"
- 10분 이내에 정점 도달
- 1시간 이내에 최고점의 5% 미만으로 폭락
- 4시간 시점에 사실상 사망
- 중앙값 궤적: first_buy → 1.0 → 0.03 → 0.01 → 0.01

### HEALTHY 패턴: "상승"
- 10분 시점에도 여전히 상승 중
- 1시간 시점에 최종 최고점의 50-80% 수준
- 4시간 시점에도 여전히 성장 가능
- 중앙값 궤적: first_buy → 0.15 → 0.19 → 0.15 → 0.08

![시가총액 궤적](charts/mcap_trajectories.png)

---

## 7. 주요 라벨링 토큰 (Dune 데이터 기반)

### 상위 10개 RUG 토큰

| # | 심볼 | 최대 시가총액 | 1시간 시가총액 | 10초 매수량 | 1분 매도량 | 1시간 하락률 |
|---|------|-------------|--------------|------------|-----------|------------|
| 1 | ASC | $5,239,791 | $427,234 | 96.0 SOL | 11.0 SOL | 92% |
| 2 | APT | $4,898,695 | $129,423 | 85.0 SOL | 0.0 SOL | 97% |
| 3 | UBER | $2,476,096 | $44,990 | 85.0 SOL | 0.0 SOL | 98% |
| 4 | Shizu | $2,314,645 | $4,505 | 1.2 SOL | 1.2 SOL | 99.8% |
| 5 | 001 | $2,259,701 | $350,716 | 85.0 SOL | 0.0 SOL | 84% |
| 6 | QFI | $1,760,941 | $10,344 | 78.4 SOL | 19.5 SOL | 99% |
| 7 | KILLA | $1,733,563 | $24,693 | 56.8 SOL | 14.4 SOL | 99% |
| 8 | America | $1,573,597 | $4,186 | 4.2 SOL | 4.2 SOL | 99.7% |
| 9 | BIOAGENT | $1,240,651 | $33,914 | 2.4 SOL | 0.0 SOL | 97% |
| 10 | 艾币 | $1,166,791 | $172,263 | 39.2 SOL | 26.3 SOL | 85% |

### 상위 10개 HEALTHY 토큰

| # | 심볼 | 최대 시가총액 | 1시간 시가총액 | 10초 매수량 | 1분 매도량 | 1시간 유지율 |
|---|------|-------------|--------------|------------|-----------|-------------|
| 1 | HTERM | $43,943,160 | $20,341,560 | 6.3 SOL | 0.6 SOL | 46% |
| 2 | Asha | $22,030,787 | $6,221,012 | 30.2 SOL | 33.1 SOL | 28% |
| 3 | ALIVE | $4,299,291 | $1,922,816 | 127.9 SOL | 42.8 SOL | 45% |
| 4 | YUMI | $3,766,797 | $499,511 | 85.0 SOL | 0.0 SOL | 13% |
| 5 | Cluster | $2,879,019 | $71,606 | 29.3 SOL | 6.7 SOL | 2.5% |
| 6 | ZUG | $2,682,809 | $93,146 | 2.2 SOL | 2.3 SOL | 3.5% |
| 7 | NEUROMRPHZ | $2,538,656 | $1,861,258 | 32.4 SOL | 0.4 SOL | 73% |
| 8 | LUMINA | $1,550,426 | $399,744 | 51.5 SOL | 23.3 SOL | 26% |
| 9 | AEGIS | $1,311,878 | $87,599 | 15.7 SOL | 15.6 SOL | 7% |
| 10 | TOONS | $1,090,394 | $540,878 | 85.0 SOL | 153.9 SOL | 50% |

---

## 8. 제안 규칙 기반 탐지 (v1)

이번 분석 결과를 토대로, **처음 60초 이내**에 사용 가능한 데이터를 활용한 간단한 점수 체계를 제안합니다:

```
SCORE = 0

# 신호 1: 처음 10초 내 대량 매수 (봇 군집)
if buy_sol_vol_10s > 50:    SCORE += 25
elif buy_sol_vol_10s > 30:  SCORE += 15

# 신호 2: 처음 1분 내 대량 매도 (내부자 수익 실현)
if sell_vol_sol_1m > 30:    SCORE += 25
elif sell_vol_sol_1m > 15:  SCORE += 15

# 신호 3: 매도/매수 비율 불균형
if sell_buy_ratio > 3.0:   SCORE += 20
elif sell_buy_ratio > 2.0: SCORE += 10

# 신호 4: 처음 5초 내 다수의 고유 지갑 (봇 군단)
if unique_wallets_5s > 10: SCORE += 15
elif unique_wallets_5s > 5: SCORE += 8

# 신호 5: 대규모 단일 매수 (한 거래에서 커브의 10%+ 채움)
if max_single_buy > 10:    SCORE += 15
elif max_single_buy > 5:   SCORE += 8

# 판정
if SCORE >= 50: "고위험 — 러그풀 가능성 높음"
if SCORE >= 30: "중위험 — 의심스러운 패턴"
if SCORE < 30:  "저위험 — 유기적으로 보임"
```

### 예상 성능 (본 데이터셋 기준):

`buy_sol_vol_10s > 30 OR sell_vol_sol_1m > 15`를 단순 규칙으로 적용 시:
- RUG 토큰의 약 65%를 탐지 (106/163)
- HEALTHY에 대한 오탐율: 약 20% (9/45)

추가 신호(지갑 클러스터링, 생성자 이력)를 결합하면 이 수치가 크게 개선될 것이며, 이는 집계된 커뮤니티 테이블이 아닌 실시간 RPC 데이터가 필요합니다.

---

## 9. 데이터 한계 및 향후 계획

### 본 분석의 범위
- 단일 날짜(2025년 1월 5일)의 47,247개 토큰
- 커뮤니티 Dune 테이블의 집계 특징 (first_buy_cnt, sell_vol_1m, 시가총액 스냅샷)
- 특정 사례에 대한 `pumpdotfun_solana.pump_evt_tradeevent`의 거래별 데이터

### 아직 측정하지 못한 것들
- **생성자 지갑 이력** — 이 생성자가 과거에 몇 개의 토큰을 출시했는가? (비용이 큰 크로스 조인 필요)
- **지갑 클러스터링** — 초기 매수자들이 동일한 출처에서 자금을 조달받았는가? (그래프 분석 필요)
- **생성자 매도 행동** — 생성자 본인이 매도했는가? (토큰별로 createevent와 tradeevent를 조인해야 함)
- **다중 날짜** — 우리 샘플은 하루치; 시장 상황에 따라 패턴이 달라질 수 있음
- **Pump.fun 자체 DEX** — Pump.fun은 현재 졸업 후 자체 AMM을 운영; 우리의 dex_solana.trades 데이터는 이전 Raydium 마이그레이션 경로를 다룸

### 권장 후속 단계
1. **라벨링 데이터셋 확장** — 여러 주에 걸쳐 자체 라벨링 쿼리를 실행하여 클래스당 1,000개 이상의 토큰 확보
2. **토큰별 거래 특징 추출** — 모든 라벨링 토큰에 대해 처음 60초 거래 패턴을 얻기 위한 배치 Dune 쿼리 작성 (비용이 크지만 핵심)
3. **실시간 파이프라인 구축** — Solana WebSocket → 특징 추출 → 점수 산출 → Telegram 알림
4. **최신 데이터에서 검증** — Pump.fun이 DEX를 변경했으므로; 최신 토큰은 다른 패턴을 보일 수 있음
5. **생성자 그래프 분석** — 지갑 자금 조달 패턴을 매핑하여 상습 러그풀 범인 식별

---

## 10. 사용된 Dune 쿼리

### 쿼리 1: 전체 데이터셋 개요
```sql
SELECT COUNT(*) as total, 
  COUNT(CASE WHEN max_mcap < 7000 THEN 1 END) as dead_on_arrival,
  COUNT(CASE WHEN max_mcap >= 100000 THEN 1 END) as high_traction
FROM dune.bumaye17.result_clean_pump_fun
```

### 쿼리 2: 라벨링 토큰 추출
```sql
SELECT account_mint, symbol, created_time, created_user,
  first_buy_cnt, first_buy_vol_sol, buy_sol_vol_10s, sell_vol_sol_1m,
  mcap_first_buy, mcap_10m, mcap_1h, mcap_4h, mcap_12h, 
  last_mcap, max_mcap, max_mcap_10m
FROM dune.bumaye17.result_clean_pump_fun
WHERE max_mcap > 10000
ORDER BY max_mcap DESC LIMIT 500
```

### 쿼리 3: 특정 토큰의 거래별 데이터
```sql
SELECT 
  COALESCE(isBuy, is_buy) as is_buy,
  CAST(COALESCE(solAmount, sol_amount) AS double) / 1e9 as sol_amt,
  CAST(COALESCE(virtualSolReserves, virtual_sol_reserves) AS double) / 1e9 as v_sol,
  user, evt_block_time
FROM pumpdotfun_solana.pump_evt_tradeevent
WHERE mint = '{MINT_ADDRESS}'
  AND evt_block_time >= CAST('2025-01-05' AS timestamp)
ORDER BY evt_block_time LIMIT 100
```

### 쿼리 4: 졸업 토큰 생존 확인
```sql
WITH graduated AS (
  SELECT mint, evt_block_time as graduated_at
  FROM pumpdotfun_solana.pump_evt_completeevent
  WHERE evt_block_time >= CAST('2025-01-15' AS timestamp)
    AND evt_block_time < CAST('2025-01-17' AS timestamp)
)
SELECT g.mint, g.graduated_at, COUNT(*) as dex_trades_7d, SUM(d.amount_usd) as dex_volume_7d
FROM graduated g
INNER JOIN dex_solana.trades d ON (d.token_bought_mint_address=*** OR d.token_sold_mint_address=***
WHERE d.block_time >= g.graduated_at AND d.block_time < g.graduated_at + INTERVAL '7' DAY
GROUP BY 1, 2 HAVING SUM(d.amount_usd) > 50000
```

### 쿼리 5: 생성자 토큰 수
```sql
SELECT user as creator, COUNT(*) as tokens_created
FROM pumpdotfun_solana.pump_evt_createevent
WHERE user IN ('{CREATOR_LIST}')
  AND evt_block_time >= CAST('2024-06-01' AS timestamp)
GROUP BY 1
```

### 쿼리 6: Pump.fun 일일 규모
```sql
SELECT COUNT(*) as total_creates
FROM pumpdotfun_solana.pump_evt_createevent
WHERE evt_block_time >= CAST('2025-01-01' AS timestamp) 
  AND evt_block_time < CAST('2025-02-01' AS timestamp)
-- Result: 2025년 1월에 1,727,508개 토큰 (일 36K개)
```

---

## 차트 목록

1. `charts/pumpfun_landscape.png` — 토큰 결과 분포 (47K 토큰)
2. `charts/rug_vs_healthy_features.png` — 9개 패널 특징 분포 비교
3. `charts/signal_strength.png` — 특징 중앙값 비교 막대 차트
4. `charts/mcap_trajectories.png` — 정규화된 시가총액 궤적 (전체 토큰 오버레이)
5. `charts/trade_by_trade_comparison.png` — $ASC (러그) vs $HTERM (건전) 첫 100개 거래
6. `charts/rugpull_charts.png` — 6개 악명 높은 러그풀 토큰의 시간별 가격 차트 (LIBRA, HAWK, TRUMP, MELANIA, JENNER, QUANT)
