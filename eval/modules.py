"""Metrics 7 and 8: obligation precision and the alert false-positive rate, scored against the
register.

    uv run python -m eval.modules              # writes eval/results/w7-module-metrics.md
    uv run python -m eval.modules --out -      # print it
    uv run python -m eval.modules --as-of 2026-12-31

Both are reported apart from the RAG metrics, and the reason is in `eval/README.md`: an alert
module can be perfect on a system that retrieves badly, and the reverse. Neither needs a judge —
the register is the ground truth, as it is for extraction — so both are exact and both run in
seconds.

What each one asks:

**Obligation precision.** Of the `obligations` rows that came from a document, the fraction whose
due date is a date the register prints on *that* document, for that person. A reminder about a
date nobody printed is a false obligation. This scores what the row says against what the
document holds, not whether every obligation that should exist does: an obligation can only be
created from a fact the extractor wrote, so recall here is bounded by extraction recall and is
reported beside the precision rather than folded into it.

The catalogue's own calendar deadlines — a filing date, a contribution cutoff — belong to no
document, so they are checked against `core/documents.yaml` instead and counted separately. The
register cannot speak for them and scoring them against it would read as a failure of the module.

**Alert false-positive rate.** Of the alerts the module fires, the fraction where the register,
recomputed independently, does not cross the declared threshold. The recomputation deliberately
duplicates `modules/alert/queries.py` over register rows rather than reusing its SQL: a metric
checked by the query that produced it is not checked at all. The thresholds themselves are read
from the catalogue, because what counts as crossing is a declaration, not an opinion of this file.

An alert can be false while every fact behind it is true. The module reads the vault, and a fact
the extractor never wrote is a date the module cannot know about; the register knows. That is the
difference this metric exists to find, and it is why the rate is scored against the register and
not against the facts table.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OBLIGATION_TARGET = 0.95  # metric 7 in eval/README.md
ALERT_TARGET = 0.05  # metric 8, a ceiling rather than a floor

Row = Mapping[str, str]


# ------------------------------------------------------------------------------- obligations


@dataclass(frozen=True, slots=True)
class Obligation:
    """One `obligations` row, with the fact and document it was created from."""

    obligation_id: int
    label: str
    due_date: date
    subject: str | None
    key: str | None  # the fact key, e.g. expiry_date; None for a calendar deadline
    doc_id: str | None  # None for a calendar deadline
    recurrence: str | None

    @property
    def from_a_document(self) -> bool:
        return self.doc_id is not None and self.key is not None


@dataclass(frozen=True, slots=True)
class Verdict:
    """What the register says about one obligation. `verdict` is the bucket it counts in."""

    obligation: Obligation
    verdict: str
    expected: str = ""

    @property
    def correct(self) -> bool:
        return self.verdict in ("matches the register", "declared in the catalogue")


def obligations(conn: Any) -> list[Obligation]:
    with conn.cursor() as cur:
        cur.execute(OBLIGATION_ROWS)
        return [
            Obligation(
                obligation_id=int(row[0]),
                label=str(row[1]),
                due_date=row[2],
                subject=None if row[3] is None else str(row[3]),
                key=None if row[4] is None else str(row[4]),
                doc_id=None if row[5] is None else str(row[5]),
                recurrence=None if row[6] is None else str(row[6]),
            )
            for row in cur.fetchall()
        ]


# Hand-written and parameterless, as AGENTS.md rule 1 requires. A calendar obligation has no
# `fact_id`, so the joins are outer: it must come back as a row with nulls, not be filtered away.
OBLIGATION_ROWS = """
SELECT o.id,
       o.label,
       o.due_date,
       f.subject,
       f.key,
       regexp_replace(d.original_name, '\\.[^.]+$', '') AS doc_id,
       o.recurrence
  FROM obligations o
  LEFT JOIN facts f ON f.id = o.fact_id
  LEFT JOIN documents d ON d.id = f.document_id
 ORDER BY o.due_date, o.id
"""


def _same_person(left: str | None, right: str | None) -> bool:
    """A passport prints RACHEL NG HUI SHAN and the register writes Rachel Ng Hui Shan. Case is
    not a disagreement about who someone is; a different name is."""
    return (left or "").strip().casefold() == (right or "").strip().casefold()


def score_obligations(
    rows: Sequence[Obligation], register: Sequence[Row], declared: Sequence[Any]
) -> list[Verdict]:
    """One verdict per obligation. `declared` is the catalogue's `registers.reminder` configs."""
    by_doc = {(row.get("doc_id") or ""): row for row in register}
    calendar = {
        (config.key.replace("_", " "), config.on_date)
        for config in declared
        if config.on_date is not None
    }
    out: list[Verdict] = []
    for row in rows:
        if not row.from_a_document:
            verdict = (
                "declared in the catalogue"
                if (row.label.strip(), row.due_date) in calendar
                else "no catalogue deadline says so"
            )
            out.append(Verdict(row, verdict, expected="core/documents.yaml"))
            continue
        entry = by_doc.get(row.doc_id or "")
        if entry is None:
            out.append(Verdict(row, "no register row for that document"))
            continue
        printed = (entry.get(row.key or "") or "").strip()
        if not printed:
            out.append(Verdict(row, "the register leaves that field empty"))
        elif printed != row.due_date.isoformat():
            out.append(Verdict(row, "a date the document does not print", expected=printed))
        elif not _same_person(row.subject, entry.get("subject")):
            out.append(Verdict(row, "the wrong person", expected=entry.get("subject") or ""))
        else:
            out.append(Verdict(row, "matches the register", expected=printed))
    return out


def obligation_precision(verdicts: Sequence[Verdict]) -> float | None:
    """Metric 7, over the obligations a document produced. A calendar deadline is excluded: it
    has no document, so it is neither evidence for nor against the extraction it did not use."""
    scored = [v for v in verdicts if v.obligation.from_a_document]
    if not scored:
        return None
    return round(sum(v.correct for v in scored) / len(scored), 4)


def obligations_possible(register: Sequence[Row], declared: Sequence[Any]) -> int:
    """How many document-derived obligations the register supports — the denominator precision
    does *not* use, reported beside it so a precision of 1.0 over three rows cannot be mistaken
    for a reminder system that found everything."""
    fields = {config.from_field for config in declared if config.from_field}
    return sum(1 for row in register for field in fields if (row.get(field) or "").strip())


# ------------------------------------------------------------------------------- alerts


@dataclass(frozen=True, slots=True)
class Measured:
    """A metric recomputed from the register, for one person and one of their things.

    `note` is the counter-evidence in words. A false positive is only useful if it says what the
    register knew instead — "cover runs to 2027-02-28" is a finding; "no value" is a shrug.
    """

    value: Decimal
    subject: str | None = None
    item: str | None = None
    note: str = ""

    @property
    def key(self) -> tuple[str | None, str | None]:
        return self.subject, self.item


@dataclass(frozen=True, slots=True)
class AlertVerdict:
    metric: str
    subject: str | None
    item: str | None
    fired_value: Decimal
    register_value: Decimal | None
    crosses: bool  # whether the register's own value crosses the declared threshold
    ceiling: float
    reason: str = ""

    @property
    def false_positive(self) -> bool:
        return not self.crosses


def _number(value: str | None) -> Decimal | None:
    try:
        return Decimal((value or "").strip().replace(",", ""))
    except (InvalidOperation, ValueError):
        return None


def _day(value: str | None) -> date | None:
    try:
        return date.fromisoformat((value or "").strip())
    except ValueError:
        return None


def register_days_uncovered(register: Sequence[Row], today: date) -> list[Measured]:
    """Days since cover lapsed, per person and per policy, from the register's own expiry dates.

    The latest expiry for a policy wins, exactly as the module does it: a renewal notice printing
    last year's expiry does not mean the policy lapsed, and grouping by person alone would let a
    live travel policy cover a lapsed motor one.

    Unlike the module, a policy still in force is returned too, as a negative gap. The module has
    no reason to carry one and filters it out; here it is the counter-evidence for a false
    positive, and `ceiling: 0` means a negative value does not cross the threshold either way, so
    the verdict is unchanged by keeping it.
    """
    latest: dict[tuple[str | None, str | None], date] = {}
    for row in register:
        expiry = _day(row.get("expiry_date"))
        if expiry is None:
            continue
        key = (row.get("subject"), (row.get("policy_no") or "").strip() or None)
        held = latest.get(key)
        if held is None or expiry > held:
            latest[key] = expiry
    return [
        Measured(
            Decimal((today - expiry).days),
            subject,
            item,
            note=f"the register's latest expiry for it is {expiry.isoformat()}",
        )
        for (subject, item), expiry in latest.items()
    ]


def register_srs_contributions_ytd(register: Sequence[Row], today: date) -> list[Measured]:
    """Each holder's largest year-to-date total for the year being swept. A statement restates
    the total rather than adding to it, so these are not summed."""
    best: dict[str | None, Decimal] = {}
    for row in register:
        amount = _number(row.get("contributions_ytd"))
        year = _number(row.get("statement_year"))
        if amount is None or year is None or int(year) != today.year:
            continue
        subject = row.get("subject")
        if subject not in best or amount > best[subject]:
            best[subject] = amount
    return [Measured(value, subject) for subject, value in best.items()]


def register_donations_ytd(register: Sequence[Row], today: date) -> list[Measured]:
    """Deductible donations this year, added up. A receipt that does not say it is deductible is
    not counted — relief claimed on a donation that does not qualify is the costlier mistake."""
    totals: dict[str | None, Decimal] = {}
    for row in register:
        amount = _number(row.get("donation_amount"))
        when = _day(row.get("donation_date"))
        deductible = (row.get("tax_deductible") or "").strip().casefold() == "true"
        if amount is None or when is None or when.year != today.year or not deductible:
            continue
        totals[row.get("subject")] = totals.get(row.get("subject"), Decimal(0)) + amount
    return [Measured(value, subject) for subject, value in totals.items()]


def register_cpf_contributions_ytd(register: Sequence[Row], today: date) -> list[Measured]:
    """Employee CPF on this year's payslips, added up. `pay_period` is text, as YYYY-MM."""
    totals: dict[str | None, Decimal] = {}
    for row in register:
        amount = _number(row.get("cpf_employee"))
        period = (row.get("pay_period") or "").strip()
        if amount is None or period[:4] != str(today.year):
            continue
        totals[row.get("subject")] = totals.get(row.get("subject"), Decimal(0)) + amount
    return [Measured(value, subject) for subject, value in totals.items()]


# Mirrors `modules.alert.METRICS` over the register. A metric declared in the catalogue with no
# entry here cannot be scored, and `score_alerts` says so rather than passing it.
REGISTER_METRICS: dict[str, Callable[[Sequence[Row], date], list[Measured]]] = {
    "days_uncovered": register_days_uncovered,
    "srs_contributions_ytd": register_srs_contributions_ytd,
    "donations_ytd": register_donations_ytd,
    "cpf_contributions_ytd": register_cpf_contributions_ytd,
}


def score_alerts(fired: Sequence[Any], register: Sequence[Row], today: date) -> list[AlertVerdict]:
    """One verdict per fired alert: whether the register, recomputed, crosses the same threshold.

    `fired` is `modules.alert.Alert`, which carries the ceiling and `warn_at` it fired against,
    so the threshold is the catalogue's and not this file's.
    """
    # The module's own rule for what crossing means, imported rather than restated. The
    # recomputation of the *value* must be independent — that is the whole check — but the
    # *threshold rule* is a declaration, and a second copy of it here would make this metric fail
    # whenever the two copies drifted, which is not what it is measuring. The cost, stated: a bug
    # in `_triggered` is invisible to this number and has to be found by reading it.
    from core.contracts import AlertConfig
    from modules.alert import Measurement, _triggered

    out: list[AlertVerdict] = []
    for alert in fired:
        compute = REGISTER_METRICS.get(alert.metric)
        if compute is None:
            out.append(
                AlertVerdict(
                    alert.metric,
                    alert.subject,
                    alert.item,
                    alert.value,
                    None,
                    crosses=True,  # unscorable, and counting it false would be a guess
                    ceiling=alert.ceiling,
                    reason="no register equivalent of this metric; not scored",
                )
            )
            continue
        config = AlertConfig(metric=alert.metric, ceiling=alert.ceiling, warn_at=alert.warn_at)
        mine = {m.key: m for m in compute(register, today)}
        measured = mine.get((alert.subject, alert.item))
        if measured is None:
            out.append(
                AlertVerdict(
                    alert.metric,
                    alert.subject,
                    alert.item,
                    alert.value,
                    None,
                    crosses=False,
                    ceiling=alert.ceiling,
                    reason="the register produces no value at all for this person and item",
                )
            )
            continue
        # `Measurement` carries citations and the register has none to give, so only the value
        # crosses over: the threshold rule is the module's, the number being tested is mine.
        crosses = _triggered(config, Measurement(measured.value))
        out.append(
            AlertVerdict(
                alert.metric,
                alert.subject,
                alert.item,
                alert.value,
                measured.value,
                crosses=crosses,
                ceiling=alert.ceiling,
                reason=(
                    ""
                    if crosses
                    else " — ".join(
                        part
                        for part in ("the register does not reach the threshold", measured.note)
                        if part
                    )
                ),
            )
        )
    return out


def alert_fpr(verdicts: Sequence[AlertVerdict]) -> float | None:
    """Metric 8. `None` when nothing fired: a rate over zero alerts is not 0.0, it is unmeasured,
    and reporting 0.0 would let a module that never fires claim the target."""
    if not verdicts:
        return None
    return round(sum(v.false_positive for v in verdicts) / len(verdicts), 4)


# ------------------------------------------------------------------------------- both at once


@dataclass(frozen=True, slots=True)
class ModuleMetrics:
    """What `eval.run` puts in a result file, and what the W7 report prints."""

    as_of: date
    obligations: list[Verdict]
    alerts: list[AlertVerdict]
    possible: int
    due_today: int  # inside a lead window on `as_of`
    overdue: int

    @property
    def precision(self) -> float | None:
        return obligation_precision(self.obligations)

    @property
    def fpr(self) -> float | None:
        return alert_fpr(self.alerts)

    def as_dict(self) -> dict[str, Any]:
        """The detail that goes beside the two numbers, so a run file explains its own score."""
        buckets: dict[str, int] = {}
        for verdict in self.obligations:
            buckets[verdict.verdict] = buckets.get(verdict.verdict, 0) + 1
        return {
            "as_of": self.as_of.isoformat(),
            "obligations": {
                "n": len(self.obligations),
                "from_a_document": sum(v.obligation.from_a_document for v in self.obligations),
                "the_register_supports": self.possible,
                "by_verdict": dict(sorted(buckets.items())),
            },
            "alerts": {
                "fired": len(self.alerts),
                "false": sum(v.false_positive for v in self.alerts),
                "each": [
                    {
                        "metric": v.metric,
                        "subject": v.subject,
                        "item": v.item,
                        "fired_value": str(v.fired_value),
                        "register_value": None
                        if v.register_value is None
                        else str(v.register_value),
                        "false_positive": v.false_positive,
                        "reason": v.reason,
                    }
                    for v in self.alerts
                ],
            },
            "reminders_on_the_day": {"due": self.due_today, "overdue": self.overdue},
        }


def measure(conn: Any, register: Sequence[Row], today: date) -> ModuleMetrics:
    """Both module metrics, from the vault and the register. Sweeps with `mark=False`: measuring
    must not consume a lead window or a debounce, or the next real sweep goes quiet."""
    from core.packs import catalog
    from modules import alert, reminder

    declared = catalog().documents.registers.reminder or []
    rows = obligations(conn)
    fired = alert.sweep(conn, today, mark=False)
    return ModuleMetrics(
        as_of=today,
        obligations=score_obligations(rows, register, declared),
        alerts=score_alerts(fired, register, today),
        possible=obligations_possible(register, declared),
        due_today=len(reminder.sweep(conn, today, mark=False)),
        overdue=len(reminder.overdue(conn, today)),
    )


# ------------------------------------------------------------------------------- the report


def _mark(value: float | None, target: float, *, ceiling: bool) -> str:
    if value is None:
        return "—"
    ok = value <= target if ceiling else value >= target
    return f"{value:.3f} {'✓' if ok else '✗'}"


def render(metrics: ModuleMetrics, *, git_sha: str, corpus_sha: str) -> str:
    """The W7 report. A pure function of the measurement, so a test needs no database."""
    scored = [v for v in metrics.obligations if v.obligation.from_a_document]
    calendar = [v for v in metrics.obligations if not v.obligation.from_a_document]
    lines = [
        f"# Module metrics — {metrics.as_of.isoformat()}",
        "",
        "Metrics 7 and 8 of `eval/README.md`, reported apart from the RAG metrics because an "
        "alert module can be perfect on a system that retrieves badly, and the reverse. Scored "
        "against `corpus/register/` by `python -m eval.modules`; corpus "
        f"`{corpus_sha}`, code `{git_sha}`. Both sweeps ran with `mark=False`, so measuring "
        "consumed no lead window and no debounce.",
        "",
        "| metric | target | measured |",
        "|---|---|---|",
        f"| Obligation precision | ≥ {OBLIGATION_TARGET:.2f} | "
        f"{_mark(metrics.precision, OBLIGATION_TARGET, ceiling=False)} |",
        f"| Alert false-positive rate | ≤ {ALERT_TARGET:.2f} | "
        f"{_mark(metrics.fpr, ALERT_TARGET, ceiling=True)} |",
        "",
        f"## Obligations — {len(scored)} from a document, {len(calendar)} from the calendar",
        "",
        f"Precision is over the {len(scored)} a document produced. The register supports "
        f"{metrics.possible} of them, so this is a precision, not a count of what was found: an "
        "obligation can only be created from a fact the extractor wrote, and the gap between "
        f"{len(scored)} and {metrics.possible} is extraction recall, not reminder logic.",
        "",
        "| due | obligation | from | verdict | the register says |",
        "|---|---|---|---|---|",
    ]
    for verdict in metrics.obligations:
        row = verdict.obligation
        source = f"`{row.doc_id}`.`{row.key}`" if row.from_a_document else "_the catalogue_"
        mark = "" if verdict.correct else " ✗"
        lines.append(
            f"| {row.due_date.isoformat()} | {row.label} | {source} | {verdict.verdict}{mark} | "
            f"{verdict.expected or '—'} |"
        )
    lines += [
        "",
        f"On {metrics.as_of.isoformat()} the reminder sweep had {metrics.due_today} obligation(s) "
        f"inside a lead window and {metrics.overdue} overdue. Those counts move with the date; "
        "the precision above does not, which is why it is the number in the table.",
        "",
        "## Alerts",
        "",
    ]
    if not metrics.alerts:
        lines += [
            "Nothing fired, so the rate is unmeasured rather than 0.00 — a module that never "
            "fires would otherwise claim the target. The declared thresholds are in "
            "`core/documents.yaml` under `registers.alert`.",
            "",
        ]
    else:
        lines += [
            "| metric | whose | item | fired at | the register says | verdict |",
            "|---|---|---|---|---|---|",
        ]
        for alert in metrics.alerts:
            says = "—" if alert.register_value is None else str(alert.register_value)
            mark = "false positive ✗" if alert.false_positive else "correct"
            lines.append(
                f"| `{alert.metric}` | {alert.subject or 'household'} | {alert.item or '—'} | "
                f"{alert.fired_value} | {says} | {mark} |"
            )
        lines.append("")
        if any(a.metric == "days_uncovered" for a in metrics.alerts):
            lines += [
                "`days_uncovered` counts days since cover lapsed, so a negative value in the "
                "register column is cover still to run rather than a gap.",
                "",
            ]
        for alert in metrics.alerts:
            if alert.reason:
                lines.append(
                    f"- `{alert.metric}` for {alert.subject or 'household'}: {alert.reason}."
                )
        lines.append("")
    lines += ["## How to read it", "", PLACEHOLDER, ""]
    return "\n".join(lines)


PLACEHOLDER = "_(one paragraph, written on the day)_"


def _paragraph(target: Path) -> str:
    """The prose under "How to read it" from the file already there, if someone wrote one."""
    if not target.exists():
        return ""
    after = target.read_text(encoding="utf-8").partition("## How to read it")[2].strip()
    return "" if not after or after == PLACEHOLDER else after


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--out",
        default=str(ROOT / "eval" / "results" / "w7-module-metrics.md"),
        help="file to write, or - for stdout (default eval/results/w7-module-metrics.md)",
    )
    parser.add_argument(
        "--as-of",
        default="",
        help="the date to sweep for, YYYY-MM-DD (default today). Both metrics are date-dependent",
    )
    args = parser.parse_args(argv)

    sys.path.insert(0, str(ROOT))
    from core.runtime.db import DatabaseUnavailable, connect
    from core.runtime.settings import ConfigurationError, Settings
    from eval.run import _corpus_sha, _git_sha
    from eval.sets_io import read_registers

    try:
        today = date.fromisoformat(args.as_of) if args.as_of else datetime.now(UTC).date()
    except ValueError:
        parser.error(f"--as-of takes a date as YYYY-MM-DD, not {args.as_of!r}")
    try:
        settings = Settings.load(ROOT)
        register = read_registers(ROOT)
        with connect(settings) as conn:
            metrics = measure(conn, register, today)
    except ConfigurationError as error:
        print(f"Configuration needs attention: {error}")
        return 2
    except DatabaseUnavailable as error:
        print(error)
        return 2

    report = render(metrics, git_sha=_git_sha(), corpus_sha=_corpus_sha(ROOT))
    if args.out == "-":
        print(report)
        return 0
    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    keep = _paragraph(target)
    target.write_text(report.replace(PLACEHOLDER, keep) if keep else report, encoding="utf-8")
    print(
        f"obligation_precision {metrics.precision if metrics.precision is not None else '—'}"
        f"  (target >= {OBLIGATION_TARGET:.2f})"
    )
    print(
        f"alert_fpr {metrics.fpr if metrics.fpr is not None else '— nothing fired'}"
        f"  (target <= {ALERT_TARGET:.2f})"
    )
    print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
