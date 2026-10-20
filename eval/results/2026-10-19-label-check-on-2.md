# label-check-on-2 — 2026-10-19

Sets A, B; retrieval hybrid, reranker cross-encoder; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `8f7e6c432f1f7497`; code `bc8eee8`.

What changed, what moved, and whether that was expected:

The second measurement of ADR 0021's label check, switch **on**, with the two fixes the first
([`2026-10-19-label-check-on`](2026-10-19-label-check-on.md)) called for. A value the question
names is no longer checked, and a check that cannot run leaves its sentence unchecked. Against
[`2026-10-19-label-check-off-2`](2026-10-19-label-check-off-2.md), with the same commit and vault,
run straight after it:

| Condition for turning it on (ADR 0021) | off | on | met? |
|---|---|---|---|
| Unsupported claims fall | 15/76 | **13/76** | yes |
| Right and cited moves at most one question | 42/51 | 42/51 | yes (0) |
| Over-caution moves at most one question | 4/51 | 5/51 | yes (+1) |
| Median latency rises at most one second | 3.26 s | 3.48 s | yes (+0.22 s; p90 5.23 → 5.76 s) |

**Every condition is met. Two answers changed, and both are the check doing its job.**

- `b-b14`, "When is the road tax on SLK 8842 D due?", is no longer answered with
  `Period of Insurance From: 12 April 2026`. It is held back, and one Set B claim goes.
- `a-gen-b2-0003-expiry_date` had answered *wrongly*, quoting the renewal notice's date. It is now
  held back. That is the single over-caution step: a wrong answer turned into no answer, which
  is what the aim asks for.

**The first run's two defects are gone.** `a-gen-b2-0011-lender` keeps its right answer, because
the facility number the question names is no longer checked. `a-b08` answered in full. Its earlier
failure did not recur, so this run does not exercise the fail-safe path; the test does.

**Still missed:** `b-b06`. The judge passes `Name of Insured` as the named driver, as before. Two
of the four open car claims were in reach of this check (ADR 0021), and it catches one of them.

Turning it on is ADR 0021's decision, and its reviewers'. This run is the evidence for it.
