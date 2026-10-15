"""Put the Lim household's synthetic calendar on this computer, for the demonstration.

    uv run python scripts/seed_calendar.py           # replace the seeded entries
    uv run python scripts/seed_calendar.py --forget  # remove them and add nothing

Every entry here is invented and agrees with `corpus/canon.md`: the five people, their dates of
birth, Ah Kow's diabetes and hypertension, Mei Ling's osteoporosis, Lucas in Primary 1 in
Tampines. They are written with `created_via = 'seed'`, so running this again replaces only its
own rows and never an entry a person typed (ADR 0020). Deadlines are not seeded: they come off
the documents, as `obligations`, and the calendar reads them from there.

Entries are for a person by the first word of their name as the household roster has it. A name
the roster does not hold (an install set up with other people) makes that entry the household's,
which is how it would read anyway.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# One entry a line: title | first date | start | end | whose | where | repeat | until | last day.
# Whose is a word of the person's name; empty fields are none. October to December 2026, the weeks
# either side of the demonstration, then birthdays yearly from each canon date of birth.
ENTRIES = """
Swimming lesson | 2026-10-03 | 09:00 | 10:00 | Lucas | Tampines West CC | weekly | 2026-12-19 |
Chinese class | 2026-10-07 | 16:30 | 18:00 | Lucas | Our Tampines Hub | weekly | 2026-11-18 |
Taiji class | 2026-10-01 | 07:30 | 08:30 | Mei | Blk 45B void deck | weekly | |
Family dinner | 2026-10-18 | 18:30 | 20:30 | | Tampines Mall | monthly | |
Medication refill | 2026-10-05 | | | Kow | Tampines Polyclinic pharmacy | monthly | |
Fasting blood test | 2026-10-20 | 08:00 | 08:30 | Kow | Tampines Polyclinic | never | |
Diabetes and BP review | 2026-10-22 | 10:00 | 11:00 | Kow | Tampines Polyclinic | never | |
Diabetic eye screening | 2026-11-26 | 14:00 | 15:00 | Kow | Tampines Polyclinic | never | |
Bone density scan | 2026-11-12 | 09:30 | 10:30 | Mei | Changi General Hospital | never | |
Physiotherapy follow-up | 2026-10-29 | 15:00 | 16:00 | Mei | Changi General Hospital | never | |
Dental check-up | 2026-10-27 | 15:30 | 16:00 | Lucas | Tampines Polyclinic | never | |
Parent-teacher meeting | 2026-10-30 | 14:00 | 14:30 | Lucas | Lucas's primary school | never | |
Swimming test, level 2 | 2026-11-28 | 09:00 | 10:00 | Lucas | Tampines West CC | never | |
Last day of school term | 2026-11-20 | | | Lucas | | never | |
Car servicing, SLK 8842 D | 2026-10-24 | 10:00 | 12:00 | Marcus | Ubi workshop | never | |
Year-end town hall | 2026-12-04 | 14:00 | 16:00 | Marcus | Meridian Systems | never | |
Continuing education course | 2026-11-07 | | | Rachel | | never | |
Team dinner | 2026-11-19 | 19:00 | 21:00 | Rachel | | never | |
Family trip to Penang | 2026-12-12 | | | | Penang | never | | 2026-12-16
Christmas Day | 2026-12-25 | | | | | never | |
Marcus's birthday | 1987-05-08 | | | Marcus | | yearly | |
Rachel's birthday | 1989-02-17 | | | Rachel | | yearly | |
Lucas's birthday | 2019-06-14 | | | Lucas | | yearly | |
Ah Kow's birthday | 1958-10-12 | | | Kow | | yearly | |
Mei Ling's birthday | 1961-04-25 | | | Mei | | yearly | |
"""


def entries() -> list[list[str | None]]:
    return [
        [cell.strip() or None for cell in line.split("|")] for line in ENTRIES.strip().splitlines()
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--forget", action="store_true", help="remove the seeded entries only")
    args = parser.parse_args(argv)

    sys.path.insert(0, str(ROOT))
    from core import calendar, household
    from core.runtime.db import DatabaseUnavailable, connect
    from core.runtime.settings import Settings

    try:
        with connect(Settings.load(ROOT)) as conn:
            gone = calendar.forget_seeded(conn)
            if args.forget:
                conn.commit()
                print(f"Removed {gone} seeded entries.")
                return 0
            people = [p for p in household.roster(conn) if not p.external]

            def whose(word: str | None) -> int | None:
                if word is None:
                    return None
                for person in people:
                    names = " ".join((person.display_name, *person.aliases)).lower().split()
                    if word.lower() in names:
                        return person.id
                return None

            rows = entries()
            for title, first, start, end, who, where, repeat, until, last in rows:
                calendar.create(
                    conn,
                    calendar.EventFields(
                        title=title or "",
                        starts_on=date.fromisoformat(first or ""),
                        ends_on=date.fromisoformat(last) if last else None,
                        start_time=time.fromisoformat(start) if start else None,
                        end_time=time.fromisoformat(end) if end else None,
                        location=where,
                        person_id=whose(who),
                        repeat=repeat,  # type: ignore[arg-type]
                        repeat_until=date.fromisoformat(until) if until else None,
                    ),
                    created_via="seed",
                )
            conn.commit()
            unplaced = sorted({row[4] for row in rows if row[4] and whose(row[4]) is None})
            print(f"Seeded {len(rows)} entries (replaced {gone}).")
            if unplaced:
                print(f"No one in the roster is called {', '.join(unplaced)}; theirs are shared.")
            return 0
    except DatabaseUnavailable as error:
        print(str(error))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
