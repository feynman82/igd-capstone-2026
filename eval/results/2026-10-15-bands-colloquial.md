# bands-colloquial — 2026-10-15

Replayed from `eval/results/2026-10-15-floor-off-colloquial.json`, checked against `eval/results/2026-10-14-production-colloquial.json`. Generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `qwen2.5:7b-instruct`; corpus `f5964ce1c1ae5cf2`; git `b53f7a5`, replayed by bands at `b53f7a5`. Axis **cosine**; edges high `0.42,insurance_agent=0.45`, medium `0.38`, hard `0.32`.

## Replay check

Today's fixed floor, replayed from the floor-off run: 92 questions compared with production, 1 differ.

- `a-b17`: production answered, replay held back — documents on file: same evidence; production answered from the documents on file, a branch replay cannot see

## Set C: leaked via quote

- `c-c05`: '2,000,000'
- `c-c07`: '890', 'Tan Mei Ling'
- `c-c08`: '11 April 2027', 'MV-2026-448120'
- `c-c14`: '8200', '8,200'

These are Siew's to judge.

## Are the labels honest?

| Band | Right document | 
|---|---|
| High | 0.469 (45/96) |
| Medium | 0.133 (4/30) |
| Low | 0.000 (0/10) |

Honest.

## Today against banded

### all

| | Today (fixed floor) | Banded top 3 | Δ |
|---|---|---|---|
| Set A answered | 0.860 (43/50) | 0.860 (43/50) | tied (+0 q) |
| Set A top-3 hit | — | 0.980 (49/50) |  |
| Set A right document in High | — | 0.900 (45/50) |  |
| Set A nothing shown | 0.140 (7/50) | 0.000 (0/50) | -7 q (-0.140) |
| Set A faithfulness (answered) | 0.899 | 0.899 | +0.000 (judge noise is about 0.05) |
| Set A answer relevancy (answered) | 0.750 | 0.750 | +0.000 (judge noise is about 0.05) |
| Set B generated-answer abstention | 0.556 (15/27) | 0.556 (15/27) | tied (+0 q) |
| Set B nothing shown | 0.556 (15/27) | 0.000 (0/27) | -15 q (-0.556) |
| Set B bands shown | {} | {'Medium': 18, 'High': 46, 'Low': 8} |  |

### iras_tax

| | Today (fixed floor) | Banded top 3 | Δ |
|---|---|---|---|
| Set A answered | 0.667 (2/3) | 0.667 (2/3) | tied (+0 q) |
| Set A top-3 hit | — | 1.000 (3/3) |  |
| Set A right document in High | — | 0.667 (2/3) |  |
| Set A nothing shown | 0.333 (1/3) | 0.000 (0/3) | tied (-1 q) |
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
| Set A answered | 0.829 (29/35) | 0.829 (29/35) | tied (+0 q) |
| Set A top-3 hit | — | 0.971 (34/35) |  |
| Set A right document in High | — | 0.886 (31/35) |  |
| Set A nothing shown | 0.171 (6/35) | 0.000 (0/35) | -6 q (-0.171) |
| Set A faithfulness (answered) | 0.851 | 0.851 | +0.000 (judge noise is about 0.05) |
| Set A answer relevancy (answered) | 0.742 | 0.742 | +0.000 (judge noise is about 0.05) |
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
| 0.30 | 0.667 (2/3) | 0.750 (3/4) | 1.000 (3/3) | 0.000 (0/3) | 0.000 (0/4) |
| 0.32 | 0.667 (2/3) | 0.750 (3/4) | 1.000 (3/3) | 0.000 (0/3) | 0.000 (0/4) |
| 0.34 | 0.667 (2/3) | 0.750 (3/4) | 1.000 (3/3) | 0.000 (0/3) | 0.250 (1/4) |
| 0.36 | 0.667 (2/3) | 0.750 (3/4) | 1.000 (3/3) | 0.000 (0/3) | 0.250 (1/4) |
| 0.38 | 0.667 (2/3) | 0.750 (3/4) | 1.000 (3/3) | 0.000 (0/3) | 0.250 (1/4) |
| 0.40 | 0.667 (2/3) | 0.750 (3/4) | 0.667 (2/3) | 0.000 (0/3) | 0.250 (1/4) |
| 0.42 | 0.667 (2/3) | 0.750 (3/4) | 0.667 (2/3) | 0.000 (0/3) | 0.500 (2/4) |
| 0.44 | 0.667 (2/3) | 0.750 (3/4) | 0.667 (2/3) | 0.333 (1/3) | 0.500 (2/4) |
| **0.46** | 0.667 (2/3) | 1.000 (4/4) | 0.667 (2/3) | 0.333 (1/3) | 0.750 (3/4) |
| 0.48 | 0.667 (2/3) | 1.000 (4/4) | 0.667 (2/3) | 0.333 (1/3) | 0.750 (3/4) |
| 0.50 | 0.667 (2/3) | 1.000 (4/4) | 0.667 (2/3) | 0.333 (1/3) | 1.000 (4/4) |
| 0.52 | 0.667 (2/3) | 1.000 (4/4) | 0.667 (2/3) | 0.333 (1/3) | 1.000 (4/4) |
| **0.53** | 0.667 (2/3) | 1.000 (4/4) | 0.667 (2/3) | 0.333 (1/3) | 1.000 (4/4) |
| 0.54 | 0.333 (1/3) | 1.000 (4/4) | 0.333 (1/3) | 0.667 (2/3) | 1.000 (4/4) |
| 0.56 | 0.333 (1/3) | 1.000 (4/4) | 0.333 (1/3) | 0.667 (2/3) | 1.000 (4/4) |
| 0.58 | 0.333 (1/3) | 1.000 (4/4) | 0.333 (1/3) | 0.667 (2/3) | 1.000 (4/4) |
| 0.60 | 0.000 (0/3) | 1.000 (4/4) | 0.000 (0/3) | 1.000 (3/3) | 1.000 (4/4) |

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

Keeps today's Set A answered count up to **0.450**; meets Set B's 0.95 from **—**. Neither is chosen here.

| Edge | A answered | B abstention | A top-3 hit | A nothing shown | B nothing shown |
|---|---|---|---|---|---|
| 0.30 | 0.857 (30/35) | 0.478 (11/23) | 0.971 (34/35) | 0.000 (0/35) | 0.000 (0/23) |
| 0.32 | 0.857 (30/35) | 0.478 (11/23) | 0.971 (34/35) | 0.000 (0/35) | 0.000 (0/23) |
| 0.34 | 0.857 (30/35) | 0.478 (11/23) | 0.971 (34/35) | 0.000 (0/35) | 0.000 (0/23) |
| 0.36 | 0.857 (30/35) | 0.478 (11/23) | 0.971 (34/35) | 0.000 (0/35) | 0.000 (0/23) |
| 0.38 | 0.857 (30/35) | 0.478 (11/23) | 0.971 (34/35) | 0.000 (0/35) | 0.000 (0/23) |
| 0.40 | 0.829 (29/35) | 0.478 (11/23) | 0.914 (32/35) | 0.029 (1/35) | 0.000 (0/23) |
| 0.42 | 0.829 (29/35) | 0.522 (12/23) | 0.886 (31/35) | 0.029 (1/35) | 0.087 (2/23) |
| 0.44 | 0.829 (29/35) | 0.522 (12/23) | 0.886 (31/35) | 0.029 (1/35) | 0.130 (3/23) |
| **0.45** | 0.829 (29/35) | 0.522 (12/23) | 0.886 (31/35) | 0.029 (1/35) | 0.174 (4/23) |
| 0.46 | 0.800 (28/35) | 0.522 (12/23) | 0.829 (29/35) | 0.057 (2/35) | 0.217 (5/23) |
| 0.48 | 0.743 (26/35) | 0.522 (12/23) | 0.800 (28/35) | 0.143 (5/35) | 0.217 (5/23) |
| 0.50 | 0.657 (23/35) | 0.696 (16/23) | 0.743 (26/35) | 0.229 (8/35) | 0.391 (9/23) |
| 0.52 | 0.629 (22/35) | 0.739 (17/23) | 0.657 (23/35) | 0.286 (10/35) | 0.522 (12/23) |
| 0.54 | 0.514 (18/35) | 0.739 (17/23) | 0.600 (21/35) | 0.400 (14/35) | 0.609 (14/23) |
| 0.56 | 0.486 (17/35) | 0.826 (19/23) | 0.571 (20/35) | 0.429 (15/35) | 0.696 (16/23) |
| 0.58 | 0.429 (15/35) | 0.870 (20/23) | 0.514 (18/35) | 0.486 (17/35) | 0.826 (19/23) |
| 0.60 | 0.400 (14/35) | 0.870 (20/23) | 0.486 (17/35) | 0.514 (18/35) | 0.826 (19/23) |

## Cosine against relevance

| Axis | Keeps today's A at | B abstention there | Meets B's target at | A answered there |
|---|---|---|---|---|
| cosine | 0.450 | 0.556 (15/27) | — | — |
| relevance | 0.000 | 0.518 (14/27) | 0.920 | 0.420 (21/50) |

## How to read it

_(one paragraph, written on the day)_
