"""The Alert module: a declared threshold, crossed once, citing the documents behind it.

Reads `facts`, writes only its own event trail. It never touches `facts`, never touches
retrieval, and — rule 7 — never imports from `web/` or `api/`.

Three things make an alert worth showing rather than annoying:

- **A threshold somebody declared.** `guardrails` are not the place for it and neither is code:
  core/documents.yaml says `metric: srs_contributions_ytd, ceiling: 15300, warn_at: 0.9`, and
  changing when it fires is a change to that line.
- **A debounce.** The manifest says 168 hours. A threshold does not become news again tomorrow
  because a page was re-read, and an alert that repeats daily is an alert people turn off.
- **Citations.** An alert says a number, so it names the documents that number came from. An
  uncitable alert is not shown, on the same rule as an uncitable sentence.

Every metric is measured **per person**, and a year-to-date metric for the year being swept. One
household member's statement must never move another member's limit.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from functools import partial
from typing import Any

from core.contracts import AlertConfig
from core.packs import CORE, catalog
from modules.alert import queries

log = logging.getLogger(__name__)

DEBOUNCE_HOURS = 168  # matches modules/alert/module.yaml
CITED = 3  # documents named behind a total, newest first


@dataclass(frozen=True, slots=True)
class Measurement:
    value: Decimal
    citations: list[str] = field(default_factory=list)
    subject: str | None = None
    item: str | None = None  # which of the subject's things, when they have several: a policy


@dataclass(frozen=True, slots=True)
class Alert:
    pack_id: str
    metric: str
    value: Decimal
    ceiling: float
    warn_at: float
    citations: list[str]
    subject: str | None = None
    item: str | None = None

    @property
    def key(self) -> str:
        """What the debounce is keyed on: this metric, for this person and thing, in this pack."""
        key = f"{self.pack_id}.{self.metric}.{self.subject or 'household'}"
        return f"{key}.{self.item}" if self.item else key

    @property
    def over_ceiling(self) -> bool:
        return float(self.value) > self.ceiling

    def line(self) -> str:
        share = float(self.value) / self.ceiling if self.ceiling else float("inf")
        readable = self.metric.replace("_", " ")
        head = (
            f"{readable} is {self.value}, over the {self.ceiling:g} limit"
            if self.over_ceiling
            else f"{readable} is {self.value}, {share:.0%} of the {self.ceiling:g} limit"
        )
        who = f" for {self.subject}" if self.subject else ""
        what = f" ({self.item})" if self.item else ""
        return f"{head}{who}{what} — {'; '.join(self.citations)}"


# ------------------------------------------------------------------------------ the metrics


def _year(today: date) -> dict[str, Any]:
    """The parameters every year-to-date query takes: the calendar year `today` falls in."""
    return {
        "year": today.year,
        "year_text": str(today.year),
        "year_start": date(today.year, 1, 1),
        "next_year_start": date(today.year + 1, 1, 1),
    }


def _per_subject(conn: Any, query: str, today: date) -> dict[str | None, list[tuple[Decimal, str]]]:
    """A year-to-date query's rows, as each person's `(value, citation)` pairs in query order."""
    with conn.cursor() as cur:
        cur.execute(query, _year(today))
        rows = cur.fetchall()
    grouped: dict[str | None, list[tuple[Decimal, str]]] = {}
    for subject, value, name, page in rows:
        grouped.setdefault(subject, []).append((Decimal(value), f"{name}, page {page}"))
    return grouped


def _totals(conn: Any, today: date, *, query: str) -> list[Measurement]:
    return [
        Measurement(
            sum((value for value, _ in facts), Decimal(0)),
            [citation for _, citation in facts[:CITED]],
            subject,
        )
        for subject, facts in _per_subject(conn, query, today).items()
    ]


def srs_contributions_ytd(conn: Any, today: date) -> list[Measurement]:
    """Each holder's latest year-to-date total for this year: the largest, since it only grows."""
    out: list[Measurement] = []
    for subject, facts in _per_subject(conn, queries.SRS_CONTRIBUTIONS_YTD, today).items():
        value, citation = max(facts, key=lambda fact: fact[0])
        out.append(Measurement(value, [citation], subject))
    return out


donations_ytd = partial(_totals, query=queries.DONATIONS_YTD)
cpf_contributions_ytd = partial(_totals, query=queries.CPF_CONTRIBUTIONS_YTD)


def days_uncovered(conn: Any, today: date) -> list[Measurement]:
    """Days since cover lapsed, per insured person and policy. Nothing while a policy still runs.

    Cites the document carrying the policy's latest expiry, which is the date the gap is counted
    from.
    """
    with conn.cursor() as cur:
        cur.execute(queries.DAYS_UNCOVERED)
        rows = cur.fetchall()
    latest: dict[tuple[str | None, str | None], tuple[date, str]] = {}
    for subject, policy_no, expiry, name, page in rows:
        held = latest.get((subject, policy_no))
        if held is None or expiry > held[0]:
            latest[(subject, policy_no)] = (expiry, f"{name}, page {page}")
    out: list[Measurement] = []
    for (subject, policy_no), (expiry, citation) in latest.items():
        gap = (today - expiry).days
        if gap > 0:
            out.append(Measurement(Decimal(gap), [citation], subject, policy_no))
    return out


METRICS: dict[str, Any] = {
    "srs_contributions_ytd": srs_contributions_ytd,
    "donations_ytd": donations_ytd,
    "cpf_contributions_ytd": cpf_contributions_ytd,
    "days_uncovered": days_uncovered,
}


# ------------------------------------------------------------------------------- the sweep


def _triggered(config: AlertConfig, measurement: Measurement) -> bool:
    """`warn_at` is a share of the ceiling. A ceiling of zero means any value at all is news."""
    if config.ceiling <= 0:
        return float(measurement.value) > 0
    return float(measurement.value) >= config.ceiling * config.warn_at


def _debounced(conn: Any, alert: Alert, now: datetime, hours: int) -> bool:
    with conn.cursor() as cur:
        cur.execute(queries.LAST_FIRED, {"key": alert.key})
        row = cur.fetchone()
    if row is None:
        return False
    fired_at, payload = row
    if now - fired_at < timedelta(hours=hours):
        previous = payload.get("value") if isinstance(payload, dict) else None
        log.info(
            "alert %s is debounced (last fired at %s, value %s)", alert.key, fired_at, previous
        )
        return True
    return False


def sweep(
    conn: Any,
    today: date | None = None,
    *,
    mark: bool = True,
    debounce_hours: int = DEBOUNCE_HOURS,
    configs: tuple[AlertConfig, ...] | None = None,
) -> list[Alert]:
    """Every declared threshold that is crossed, has evidence, and has not just been said.

    `configs` defaults to the core catalogue's `registers.alert`: documents are the core's, so no
    pack being switched off silences them (ADR 0017). A test hands its own in.
    """
    now_date = today or date.today()
    now = datetime.now(UTC)
    firing: list[Alert] = []

    declared = configs if configs is not None else catalog().documents.registers.alert or []
    for config in declared:
        metric = METRICS.get(config.metric)
        if metric is None:
            log.warning(
                "the catalogue declares the metric %r, which no query in "
                "modules/alert/queries.py defines; it cannot fire",
                config.metric,
            )
            continue
        for measurement in metric(conn, now_date):
            if not _triggered(config, measurement):
                continue
            if not measurement.citations:
                log.info("not alerting on %s: nothing to cite", config.metric)
                continue
            alert = Alert(
                pack_id=CORE,
                metric=config.metric,
                value=measurement.value,
                ceiling=config.ceiling,
                warn_at=config.warn_at,
                citations=measurement.citations,
                subject=measurement.subject,
                item=measurement.item,
            )
            if _debounced(conn, alert, now, debounce_hours):
                continue
            firing.append(alert)

    if mark and firing:
        with conn.cursor() as cur:
            for alert in firing:
                cur.execute(
                    queries.RECORD_FIRED,
                    {
                        "key": alert.key,
                        "payload": json.dumps(
                            {
                                "pack_id": alert.pack_id,
                                "metric": alert.metric,
                                "value": str(alert.value),
                                "ceiling": alert.ceiling,
                                "citations": alert.citations,
                            }
                        ),
                    },
                )
        conn.commit()
    return firing
