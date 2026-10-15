-- The household calendar: what the family has on, typed in by a person. ADR 0020.
--
-- Additive only. One CREATE TABLE and its indexes; nothing in 0001-0003 is altered, dropped or
-- backfilled. See rule 4 in AGENTS.md.
--
-- Deadlines are not stored here. A renewal or a tax date is already an `obligations` row with a
-- fact and a page behind it, and the calendar reads it from there, so the date a document printed
-- is never copied into a second place where the two could disagree.

CREATE TABLE calendar_events (
    id           bigserial PRIMARY KEY,
    title        text NOT NULL CHECK (length(btrim(title)) BETWEEN 1 AND 200),
    starts_on    date NOT NULL,
    -- The last day of an event that spans several, inclusive. Null is one day.
    ends_on      date CHECK (ends_on >= starts_on),
    -- Null is all day. A time with no end is an event with a start and no stated length.
    start_time   time,
    end_time     time,
    location     text,
    notes        text,
    -- Who it is for. Null is the whole household, which is most of what a family calendar holds.
    person_id    bigint REFERENCES people(id) ON DELETE SET NULL,
    -- Whole series only: an edit or a delete applies to every date (ADR 0020).
    repeat       text NOT NULL DEFAULT 'never'
                 CHECK (repeat IN ('never','daily','weekly','monthly','yearly')),
    repeat_until date CHECK (repeat_until >= starts_on),
    -- How the row came to exist. `ask` is a draft Parrot wrote and a person confirmed; nothing
    -- reaches this table without that confirmation, which is what keeps never_acts true.
    created_via  text NOT NULL DEFAULT 'form' CHECK (created_via IN ('form','ask','seed')),
    -- Where it lives. Everything is `local` today; `google` and `icloud` are the sync adapters
    -- ADR 0020 names and does not build, and `external_id` is the provider's id once synced.
    source       text NOT NULL DEFAULT 'local' CHECK (source IN ('local','google','icloud')),
    external_id  text,
    created_at   timestamptz NOT NULL DEFAULT now(),
    updated_at   timestamptz NOT NULL DEFAULT now(),
    CHECK (end_time IS NULL OR start_time IS NOT NULL),
    CHECK (repeat <> 'never' OR repeat_until IS NULL)
);

-- The one read the screens make: events that start before the end of a range. Repeating events
-- are expanded in Python, so the range's start cannot be pushed into the index.
CREATE INDEX calendar_events_starts ON calendar_events (starts_on);

-- One local row per provider event, once sync exists.
CREATE UNIQUE INDEX calendar_events_external
    ON calendar_events (source, external_id) WHERE external_id IS NOT NULL;
