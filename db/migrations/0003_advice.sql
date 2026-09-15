-- Advice: the published values a pack calculates with, the owner's consent, and the record of
-- every advice answer. Additive only: CREATE TABLE and CREATE INDEX, nothing altered. ADR 0016.

CREATE TABLE grounding_sources (
    id             bigserial PRIMARY KEY,
    pack_id        text NOT NULL,
    corpus_id      text NOT NULL,
    file           text NOT NULL,
    title          text NOT NULL,
    publisher      text NOT NULL,
    publisher_kind text NOT NULL CHECK (publisher_kind IN ('regulator','government','industry_association')),
    url            text NOT NULL,
    published_on   date,
    retrieved_on   date NOT NULL,
    applies_to     text NOT NULL,
    review_by      date NOT NULL,
    reviewed_by    text,
    reviewed_on    date,
    sha256         bytea NOT NULL,
    indexed_at     timestamptz NOT NULL DEFAULT now(),
    UNIQUE (pack_id, corpus_id, file)
);

CREATE TABLE grounding_values (
    id             bigserial PRIMARY KEY,
    source_id      bigint NOT NULL REFERENCES grounding_sources(id) ON DELETE CASCADE,
    pack_id        text NOT NULL,
    key            text NOT NULL,
    unit           text NOT NULL,
    value_num      numeric,
    value_text     text,
    qualifiers     jsonb NOT NULL DEFAULT '{}'::jsonb,
    passage        text NOT NULL,
    extracted_by   text NOT NULL CHECK (extracted_by IN ('model','person')),
    confidence     real,
    effective_from date,
    effective_to   date,
    status         text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','approved','rejected')),
    reviewed_by    text,
    reviewed_on    date,
    note           text,
    created_at     timestamptz NOT NULL DEFAULT now(),
    CHECK (status = 'pending' OR (reviewed_by IS NOT NULL AND reviewed_on IS NOT NULL))
);
CREATE INDEX grounding_values_approved ON grounding_values (pack_id, key) WHERE status = 'approved';
CREATE INDEX grounding_values_pending  ON grounding_values (created_at) WHERE status = 'pending';

CREATE TABLE advice_consents (
    id             bigserial PRIMARY KEY,
    person_id      bigint NOT NULL REFERENCES people(id) ON DELETE CASCADE,
    pack_id        text NOT NULL,
    version        text NOT NULL,
    wording_sha256 bytea NOT NULL,
    action         text NOT NULL CHECK (action IN ('granted','withdrawn')),
    channel        text NOT NULL CHECK (channel IN ('web','telegram','cli')),
    recorded_at    timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX advice_consents_latest ON advice_consents (person_id, pack_id, recorded_at DESC, id DESC);

CREATE TABLE advice_records (
    id                 bigserial PRIMARY KEY,
    thread_id          text,
    pack_id            text NOT NULL,
    pack_version       text NOT NULL,
    shape              text NOT NULL,
    subject            text NOT NULL,
    subject_person_ids bigint[] NOT NULL,
    consent_id         bigint NOT NULL REFERENCES advice_consents(id),
    outcome            text NOT NULL CHECK (outcome IN ('advised','withheld')),
    verdict            text,
    basis              jsonb NOT NULL,
    disclaimer_sha256  bytea NOT NULL,
    answer_text        text,
    created_at         timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX advice_records_thread ON advice_records (thread_id, created_at);
