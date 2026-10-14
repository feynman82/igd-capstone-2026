# bands-first-look — 2026-10-14

Replayed from `eval/results/2026-10-14-floor-off.json`, checked against `eval/results/2026-10-14-production-for-replay.json`. Generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `qwen2.5:7b-instruct`; corpus `f5964ce1c1ae5cf2`; git `b53f7a5`, replayed by bands at `b53f7a5`. Axis **cosine**; edges high `0.42,insurance_agent=0.45`, medium `0.38`, hard `0.32`.

## Replay check

Today's fixed floor, replayed from the floor-off run: 82 questions compared with production, 0 differ.


## Set C: leaked via quote

- `c-c05`: '2,000,000'
- `c-c07`: '890', 'Tan Mei Ling'
- `c-c08`: '11 April 2027', 'MV-2026-448120'
- `c-c14`: '8200', '8,200'

These are Siew's to judge.

## Are the labels honest?

| Band | Right document | 
|---|---|
| High | 0.475 (38/80) |
| Medium | 0.042 (1/24) |
| Low | 0.000 (0/6) |

Honest.

## Today against banded

### all

| | Today (fixed floor) | Banded top 3 | Δ |
|---|---|---|---|
| Set A answered | 0.950 (38/40) | 0.950 (38/40) | tied (+0 q) |
| Set A top-3 hit | — | 0.975 (39/40) |  |
| Set A right document in High | — | 0.950 (38/40) |  |
| Set A nothing shown | 0.050 (2/40) | 0.000 (0/40) | -2 q (-0.050) |
| Set A faithfulness (answered) | 0.912 | 0.912 | +0.000 (judge noise is about 0.05) |
| Set A answer relevancy (answered) | 0.770 | 0.770 | +0.000 (judge noise is about 0.05) |
| Set B generated-answer abstention | 0.556 (15/27) | 0.556 (15/27) | tied (+0 q) |
| Set B nothing shown | 0.556 (15/27) | 0.000 (0/27) | -15 q (-0.556) |
| Set B bands shown | {} | {'Medium': 18, 'High': 46, 'Low': 8} |  |

### iras_tax

| | Today (fixed floor) | Banded top 3 | Δ |
|---|---|---|---|
| Set A answered | 1.000 (2/2) | 1.000 (2/2) | tied (+0 q) |
| Set A top-3 hit | — | 1.000 (2/2) |  |
| Set A right document in High | — | 1.000 (2/2) |  |
| Set A nothing shown | 0.000 (0/2) | 0.000 (0/2) | tied (+0 q) |
| Set A faithfulness (answered) | 1.000 | 1.000 | +0.000 (judge noise is about 0.05) |
| Set A answer relevancy (answered) | 0.936 | 0.936 | +0.000 (judge noise is about 0.05) |
| Set B generated-answer abstention | 0.750 (3/4) | 0.750 (3/4) | tied (+0 q) |
| Set B nothing shown | 0.750 (3/4) | 0.000 (0/4) | -3 q (-0.750) |
| Set B bands shown | {} | {'High': 4, 'Low': 2, 'Medium': 3} |  |

### core

| | Today (fixed floor) | Banded top 3 | Δ |
|---|---|---|---|
| Set A answered | 1.000 (12/12) | 1.000 (12/12) | tied (+0 q) |
| Set A top-3 hit | — | 1.000 (12/12) |  |
| Set A right document in High | — | 1.000 (12/12) |  |
| Set A nothing shown | 0.000 (0/12) | 0.000 (0/12) | tied (+0 q) |
| Set A faithfulness (answered) | 1.000 | 1.000 | +0.000 (judge noise is about 0.05) |
| Set A answer relevancy (answered) | 0.740 | 0.740 | +0.000 (judge noise is about 0.05) |
| Set B generated-answer abstention | — | — | — |
| Set B nothing shown | — | — | — |
| Set B bands shown | {} | {} |  |

### insurance_agent

| | Today (fixed floor) | Banded top 3 | Δ |
|---|---|---|---|
| Set A answered | 0.923 (24/26) | 0.923 (24/26) | tied (+0 q) |
| Set A top-3 hit | — | 0.962 (25/26) |  |
| Set A right document in High | — | 0.923 (24/26) |  |
| Set A nothing shown | 0.077 (2/26) | 0.000 (0/26) | -2 q (-0.077) |
| Set A faithfulness (answered) | 0.861 | 0.861 | +0.000 (judge noise is about 0.05) |
| Set A answer relevancy (answered) | 0.771 | 0.771 | +0.000 (judge noise is about 0.05) |
| Set B generated-answer abstention | 0.522 (12/23) | 0.522 (12/23) | tied (+0 q) |
| Set B nothing shown | 0.522 (12/23) | 0.000 (0/23) | -12 q (-0.522) |
| Set B bands shown | {} | {'Medium': 15, 'High': 42, 'Low': 6} |  |

### none

| | Today (fixed floor) | Banded top 3 | Δ |
|---|---|---|---|
| Set A answered | — | — | — |
| Set A top-3 hit | — | — |  |
| Set A right document in High | — | — |  |
| Set A nothing shown | — | — | — |
| Set A faithfulness (answered) | — | — |  |
| Set A answer relevancy (answered) | — | — |  |
| Set B generated-answer abstention | — | — | — |
| Set B nothing shown | — | — | — |
| Set B bands shown | {} | {} |  |

## The sweep

### iras_tax (cosine)

Keeps today's Set A answered count up to **0.530**; meets Set B's 0.95 from **0.460**. Neither is chosen here.

| Edge | A answered | B abstention | A top-3 hit | A nothing shown | B nothing shown |
|---|---|---|---|---|---|
| 0.30 | 1.000 (2/2) | 0.750 (3/4) | 1.000 (2/2) | 0.000 (0/2) | 0.000 (0/4) |
| 0.32 | 1.000 (2/2) | 0.750 (3/4) | 1.000 (2/2) | 0.000 (0/2) | 0.000 (0/4) |
| 0.34 | 1.000 (2/2) | 0.750 (3/4) | 1.000 (2/2) | 0.000 (0/2) | 0.250 (1/4) |
| 0.36 | 1.000 (2/2) | 0.750 (3/4) | 1.000 (2/2) | 0.000 (0/2) | 0.250 (1/4) |
| 0.38 | 1.000 (2/2) | 0.750 (3/4) | 1.000 (2/2) | 0.000 (0/2) | 0.250 (1/4) |
| 0.40 | 1.000 (2/2) | 0.750 (3/4) | 1.000 (2/2) | 0.000 (0/2) | 0.250 (1/4) |
| 0.42 | 1.000 (2/2) | 0.750 (3/4) | 1.000 (2/2) | 0.000 (0/2) | 0.500 (2/4) |
| 0.44 | 1.000 (2/2) | 0.750 (3/4) | 1.000 (2/2) | 0.000 (0/2) | 0.500 (2/4) |
| **0.46** | 1.000 (2/2) | 1.000 (4/4) | 1.000 (2/2) | 0.000 (0/2) | 0.750 (3/4) |
| 0.48 | 1.000 (2/2) | 1.000 (4/4) | 1.000 (2/2) | 0.000 (0/2) | 0.750 (3/4) |
| 0.50 | 1.000 (2/2) | 1.000 (4/4) | 1.000 (2/2) | 0.000 (0/2) | 1.000 (4/4) |
| 0.52 | 1.000 (2/2) | 1.000 (4/4) | 1.000 (2/2) | 0.000 (0/2) | 1.000 (4/4) |
| **0.53** | 1.000 (2/2) | 1.000 (4/4) | 1.000 (2/2) | 0.000 (0/2) | 1.000 (4/4) |
| 0.54 | 0.500 (1/2) | 1.000 (4/4) | 0.500 (1/2) | 0.500 (1/2) | 1.000 (4/4) |
| 0.56 | 0.500 (1/2) | 1.000 (4/4) | 0.500 (1/2) | 0.500 (1/2) | 1.000 (4/4) |
| 0.58 | 0.500 (1/2) | 1.000 (4/4) | 0.500 (1/2) | 0.500 (1/2) | 1.000 (4/4) |
| 0.60 | 0.000 (0/2) | 1.000 (4/4) | 0.000 (0/2) | 1.000 (2/2) | 1.000 (4/4) |

### core (cosine)

Keeps today's Set A answered count up to **0.580**; meets Set B's 0.95 from **—**. Neither is chosen here.

| Edge | A answered | B abstention | A top-3 hit | A nothing shown | B nothing shown |
|---|---|---|---|---|---|
| 0.30 | 1.000 (12/12) | — | 1.000 (12/12) | 0.000 (0/12) | — |
| 0.32 | 1.000 (12/12) | — | 1.000 (12/12) | 0.000 (0/12) | — |
| 0.34 | 1.000 (12/12) | — | 1.000 (12/12) | 0.000 (0/12) | — |
| 0.36 | 1.000 (12/12) | — | 1.000 (12/12) | 0.000 (0/12) | — |
| 0.38 | 1.000 (12/12) | — | 1.000 (12/12) | 0.000 (0/12) | — |
| 0.40 | 1.000 (12/12) | — | 1.000 (12/12) | 0.000 (0/12) | — |
| 0.42 | 1.000 (12/12) | — | 1.000 (12/12) | 0.000 (0/12) | — |
| 0.44 | 1.000 (12/12) | — | 1.000 (12/12) | 0.000 (0/12) | — |
| 0.46 | 1.000 (12/12) | — | 1.000 (12/12) | 0.000 (0/12) | — |
| 0.48 | 1.000 (12/12) | — | 1.000 (12/12) | 0.000 (0/12) | — |
| 0.50 | 1.000 (12/12) | — | 1.000 (12/12) | 0.000 (0/12) | — |
| 0.52 | 1.000 (12/12) | — | 1.000 (12/12) | 0.000 (0/12) | — |
| 0.54 | 1.000 (12/12) | — | 1.000 (12/12) | 0.000 (0/12) | — |
| 0.56 | 1.000 (12/12) | — | 0.917 (11/12) | 0.000 (0/12) | — |
| **0.58** | 1.000 (12/12) | — | 0.917 (11/12) | 0.000 (0/12) | — |
| 0.60 | 0.917 (11/12) | — | 0.917 (11/12) | 0.083 (1/12) | — |

### insurance_agent (cosine)

Keeps today's Set A answered count up to **0.470**; meets Set B's 0.95 from **—**. Neither is chosen here.

| Edge | A answered | B abstention | A top-3 hit | A nothing shown | B nothing shown |
|---|---|---|---|---|---|
| 0.30 | 0.923 (24/26) | 0.478 (11/23) | 0.962 (25/26) | 0.000 (0/26) | 0.000 (0/23) |
| 0.32 | 0.923 (24/26) | 0.478 (11/23) | 0.962 (25/26) | 0.000 (0/26) | 0.000 (0/23) |
| 0.34 | 0.923 (24/26) | 0.478 (11/23) | 0.962 (25/26) | 0.000 (0/26) | 0.000 (0/23) |
| 0.36 | 0.923 (24/26) | 0.478 (11/23) | 0.962 (25/26) | 0.000 (0/26) | 0.000 (0/23) |
| 0.38 | 0.923 (24/26) | 0.478 (11/23) | 0.962 (25/26) | 0.000 (0/26) | 0.000 (0/23) |
| 0.40 | 0.923 (24/26) | 0.478 (11/23) | 0.923 (24/26) | 0.000 (0/26) | 0.000 (0/23) |
| 0.42 | 0.923 (24/26) | 0.522 (12/23) | 0.923 (24/26) | 0.000 (0/26) | 0.087 (2/23) |
| 0.44 | 0.923 (24/26) | 0.522 (12/23) | 0.923 (24/26) | 0.000 (0/26) | 0.130 (3/23) |
| 0.46 | 0.923 (24/26) | 0.522 (12/23) | 0.923 (24/26) | 0.000 (0/26) | 0.217 (5/23) |
| **0.47** | 0.923 (24/26) | 0.522 (12/23) | 0.923 (24/26) | 0.000 (0/26) | 0.217 (5/23) |
| 0.48 | 0.885 (23/26) | 0.522 (12/23) | 0.923 (24/26) | 0.038 (1/26) | 0.217 (5/23) |
| 0.50 | 0.808 (21/26) | 0.696 (16/23) | 0.846 (22/26) | 0.115 (3/26) | 0.391 (9/23) |
| 0.52 | 0.731 (19/26) | 0.739 (17/23) | 0.731 (19/26) | 0.192 (5/26) | 0.522 (12/23) |
| 0.54 | 0.577 (15/26) | 0.739 (17/23) | 0.654 (17/26) | 0.346 (9/26) | 0.609 (14/23) |
| 0.56 | 0.577 (15/26) | 0.826 (19/23) | 0.654 (17/26) | 0.346 (9/26) | 0.696 (16/23) |
| 0.58 | 0.538 (14/26) | 0.870 (20/23) | 0.615 (16/26) | 0.385 (10/26) | 0.826 (19/23) |
| 0.60 | 0.500 (13/26) | 0.870 (20/23) | 0.577 (15/26) | 0.423 (11/26) | 0.826 (19/23) |

## Cosine against relevance

| Axis | Keeps today's A at | B abstention there | Meets B's target at | A answered there |
|---|---|---|---|---|
| cosine | 0.470 | 0.593 (16/27) | — | — |
| relevance | 0.020 | 0.593 (16/27) | 0.920 | 0.525 (21/40) |

## How to read it

_(one paragraph, written on the day)_
