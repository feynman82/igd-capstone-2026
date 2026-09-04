-- PARROT initial schema. One database holds chunks, facts, agent state and the registry.
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE documents (
    id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    sha256          bytea NOT NULL UNIQUE,          -- idempotency key: rescan updates in place
    source_channel  text  NOT NULL,                 -- folder | telegram | whatsapp | drive
    original_name   text  NOT NULL,
    mime            text  NOT NULL,
    pages           int,
    doc_type        text,                           -- null until classified
    pack_id         text,                           -- null when no installed pack owns it
    status          text  NOT NULL DEFAULT 'pending',  -- pending|indexed|quarantined
    quarantine_reason text,
    ingested_at     timestamptz NOT NULL DEFAULT now(),
    synthetic       boolean NOT NULL DEFAULT false  -- test corpora are never counted as real
);

CREATE TABLE chunks (
    id           bigserial PRIMARY KEY,
    document_id  uuid NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    page         int  NOT NULL,
    ordinal      int  NOT NULL,
    context_prefix text,                            -- the one-line "what this chunk is"
    text         text NOT NULL,
    embedding    vector(768),
    tsv          tsvector GENERATED ALWAYS AS (
                     to_tsvector('english', coalesce(context_prefix,'') || ' ' || text)
                 ) STORED,
    UNIQUE (document_id, page, ordinal)
);
CREATE INDEX chunks_hnsw ON chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX chunks_tsv  ON chunks USING gin (tsv);

-- Every fact cites a document and a page. Both NOT NULL, by design.
CREATE TABLE facts (
    id           bigserial PRIMARY KEY,
    document_id  uuid NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    page         int  NOT NULL,
    pack_id      text NOT NULL,
    pack_version text NOT NULL,                     -- so a re-extraction is auditable
    key          text NOT NULL,
    subject      text,                              -- which family member / vehicle / property
    value_text   text,
    value_num    numeric,
    value_date   date,
    confidence   real NOT NULL,
    verified_by_user boolean NOT NULL DEFAULT false, -- a correction is a labelled example
    created_at   timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX facts_lookup ON facts (pack_id, key, subject);
CREATE INDEX facts_dates  ON facts (value_date) WHERE value_date IS NOT NULL;

-- A fact is a statement about the world; an obligation is a commitment to act on it.
CREATE TABLE obligations (
    id           bigserial PRIMARY KEY,
    fact_id      bigint REFERENCES facts(id) ON DELETE CASCADE,
    pack_id      text NOT NULL,
    label        text NOT NULL,
    due_date     date NOT NULL,
    lead_days    int[] NOT NULL,
    recurrence   text,
    state        text NOT NULL DEFAULT 'pending',   -- pending|notified|done|dismissed
    last_notified_at timestamptz
);
CREATE INDEX obligations_due ON obligations (due_date, state);

CREATE TABLE packs (
    id           text PRIMARY KEY,
    version      text NOT NULL,
    manifest     jsonb NOT NULL,
    enabled      boolean NOT NULL DEFAULT true,
    installed_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE modules (
    id           text PRIMARY KEY,
    version      text NOT NULL,
    manifest     jsonb NOT NULL,
    enabled      boolean NOT NULL DEFAULT true
);

-- One trace line per graph node. This file is both the evaluation dataset and the audit trail.
CREATE TABLE traces (
    id         bigserial PRIMARY KEY,
    thread_id  text,
    node       text NOT NULL,
    latency_ms int  NOT NULL,
    model      text,
    payload    jsonb NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX traces_thread ON traces (thread_id, created_at);

-- LangGraph creates its own checkpoints/checkpoint_writes/store tables in this database.
