"""The Alert module: a pack-declared threshold, crossed once, citing the documents behind it.

Reads `facts`, writes only its own event trail. It never touches `facts`, never touches
retrieval, and — rule 7 — never imports from `web/` or `api/`.

Three things make an alert worth showing rather than annoying:

- **A threshold somebody declared.** `guardrails` are not the place for it and neither is code:
  the pack says `metric: srs_contributions_ytd, ceiling: 15300, warn_at: 0.9`, and changing when
  it fires is a change to that line.
- **A debounce.** The manifest says 168 hours. A threshold does not become news again tomorrow
  because a page was re-read, and an alert that repeats daily is an alert people turn off.
- **Citations.** An alert says a number, so it names the documents that number came from. An
  uncitable alert is not shown, on the same rule as an uncitable sentence.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import Any

from core.contracts import AlertConfig
from core.packs import InstalledPack, installed_packs
from modules.alert import queries

log = logging.getLogger(__name__)

DEBOUNCE_HOURS = 168  # matches modules/alert/module.yaml


@dataclass(frozen=True, slots=True)
class Measurement:
    value: Decimal
    citations: list[str] = field(default_factory=list)
    subject: str | None = None


@dataclass(frozen=True, slots=True)
class Alert:
    pack_id: str
    metric: str
    value: Decimal
    ceiling: float
    warn_at: float
    citations: list[str]
    subject: str | None = None

    @property
    def key(self) -> str:
        """What the debounce is keyed on: this metric, for this person, in this pack."""
        return f"{self.pack_id}.{self.metric}.{self.subject or 'household'}"

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
        return f"{head}{who} — {'; '.join(self.citations)}"


# ------------------------------------------------------------------------------ the metrics


def _citations(conn: Any, pack_id: str, key: str, limit: int = 3) -> list[str]:
    with conn.cursor() as cur:
        cur.execute(queries.EVIDENCE_FOR_KEY, {"pack_id": pack_id, "key": key, "limit": limit})
        rows = cur.fetchall()
    return [f"{name}, page {page}" for name, page, _num, _dt, _subject in rows]


def srs_contributions_ytd(conn: Any, today: date) -> list[Measurement]:
    with conn.cursor() as cur:
        cur.execute(queries.SRS_CONTRIBUTIONS_YTD)
        row = cur.fetchone()
    if row is None or row[0] is None:
        return []
    return [Measurement(Decimal(row[0]), [f"{row[4]}, page {row[3]}"], row[1])]


def donations_ytd(conn: Any, today: date) -> list[Measurement]:
    with conn.cursor() as cur:
        cur.execute(queries.DONATIONS_YTD)
        row = cur.fetchone()
    if row is None or not row[1]:
        return []
    return [Measurement(Decimal(row[0]), _citations(conn, "iras_tax", "donation_amount"))]


def cpf_contributions_ytd(conn: Any, today: date) -> list[Measurement]:
    with conn.cursor() as cur:
        cur.execute(queries.CPF_CONTRIBUTIONS_YTD)
        row = cur.fetchone()
    if row is None or not row[1]:
        return []
    return [Measurement(Decimal(row[0]), _citations(conn, "iras_tax", "cpf_employee"))]


def days_uncovered(conn: Any, today: date) -> list[Measurement]:
    """Days since cover lapsed, per insured person. Zero while a policy still runs."""
    with conn.cursor() as cur:
        cur.execute(queries.DAYS_UNCOVERED, {"today": today})
        rows = cur.fetchall()
    out: list[Measurement] = []
    for subject, last_expiry, still_covered in rows:
        if still_covered is not None or last_expiry is None:
            continue
        gap = (today - last_expiry).days
        if gap > 0:
            out.append(
                Measurement(
                    Decimal(gap), _citations(conn, "insurance_agent", "expiry_date"), subject
                )
            )
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
    packs: tuple[InstalledPack, ...] | None = None,
) -> list[Alert]:
    """Every declared threshold that is crossed, has evidence, and has not just been said."""
    now_date = today or date.today()
    now = datetime.now(UTC)
    firing: list[Alert] = []

    for installed in packs if packs is not None else installed_packs():
        for config in installed.manifest.registers.alert or []:
            metric = METRICS.get(config.metric)
            if metric is None:
                log.warning(
                    "%s declares the metric %r, which no query in modules/alert/queries.py "
                    "defines; it cannot fire",
                    installed.id,
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
                    pack_id=installed.id,
                    metric=config.metric,
                    value=measurement.value,
                    ceiling=config.ceiling,
                    warn_at=config.warn_at,
                    citations=measurement.citations,
                    subject=measurement.subject,
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
