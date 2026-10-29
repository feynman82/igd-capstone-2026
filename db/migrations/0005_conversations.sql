-- Ask's past conversations, so a person can go back to one.
--
-- Additive only. One CREATE TABLE and its index; nothing in 0001-0004 is altered, dropped or
-- backfilled. See rule 4 in AGENTS.md.
--
-- A transcript, not evidence. `messages` is the conversation as the Ask screen drew it — each
-- verified sentence with the citations it arrived with — so reopening one shows what was seen.
-- Nothing reads it back as a source: it is never retrieved, cited or extracted from, and a later
-- answer cannot lean on an earlier one. Facts stay in `facts`, with their page.

CREATE TABLE conversations (
    -- The thread id the screen sends with every question. The graph's checkpointer and the
    -- advice records are keyed on the same string, so one id names one conversation everywhere.
    id          text PRIMARY KEY CHECK (id ~ '^[A-Za-z0-9_-]{1,64}$'),
    -- The first question, shortened. Written by the API, never typed in.
    title       text NOT NULL CHECK (length(btrim(title)) BETWEEN 1 AND 200),
    messages    jsonb NOT NULL CHECK (jsonb_typeof(messages) = 'array'),
    created_at  timestamptz NOT NULL DEFAULT now(),
    updated_at  timestamptz NOT NULL DEFAULT now()
);

-- The one list the screen reads: the most recently used first.
CREATE INDEX conversations_recent ON conversations (updated_at DESC);
