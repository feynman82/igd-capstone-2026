-- The household: who lives here, what they are called on paper, and which one is you.
--
-- Additive only. Four CREATE TABLEs and their indexes; nothing here alters, drops or
-- backfills anything in 0001. See ADR 0011 and rule 4 in AGENTS.md.
--
-- The thing to understand before reading it: `facts.subject` is the string a document
-- printed, and it stays that way. This schema does not normalise it, rewrite it, or point at
-- it with a foreign key. It sits beside it and maps it, so that what a page said and what we
-- later decided it meant are two separate records and can disagree out loud.

CREATE TABLE people (
    id           bigserial PRIMARY KEY,
    -- What a person is called on screen. Theirs to choose, and not required to match any
    -- document: "Dad" is a better label on Today than "LIM AH KOW" and resolves the same.
    display_name text NOT NULL,
    -- Relation to the owner, not to the household. "self" is the owner; there is exactly one,
    -- enforced below. The list is deliberately short: these are the distinctions that change
    -- what a pack does — parent relief needs a parent, a child policy needs a child — and not
    -- a family tree. Anything finer is `other` plus a display name.
    relation     text NOT NULL CHECK (relation IN ('self','partner','child','parent','other')),
    is_owner     boolean NOT NULL DEFAULT false,
    -- A person the household has decided is NOT one of them: the ex-landlord on a tenancy
    -- agreement, a former employer, the other driver in a claim. Kept rather than discarded so
    -- their documents stop raising the same question every time one is filed.
    external     boolean NOT NULL DEFAULT false,
    created_at   timestamptz NOT NULL DEFAULT now(),
    CHECK (NOT (is_owner AND external))
);

-- Exactly one owner, held by the database rather than by application code, because "who is
-- me" is the question every first-person answer is scoped by and two of them is not a state
-- any screen knows how to render.
CREATE UNIQUE INDEX people_one_owner ON people (is_owner) WHERE is_owner;

-- Every literal string a document has printed for this person.
--
-- `alias` is compared case-insensitively and with surrounding whitespace stripped, which is
-- what the unique index is on. It is NOT otherwise normalised: no initial-expansion, no
-- reordering of "Lim, Marcus", no accent folding. Those are guesses, and a guess belongs in
-- `source = 'model'` where a person can see it and disagree, not in an index where nobody can.
CREATE TABLE person_aliases (
    id         bigserial PRIMARY KEY,
    person_id  bigint NOT NULL REFERENCES people(id) ON DELETE CASCADE,
    alias      text   NOT NULL,
    -- How this alias came to point at this person.
    --   setup   the owner typed it on the first-run screen
    --   model   the generator proposed it when an unknown subject appeared
    --   user    a person answered the question on Today, or edited the roster
    source     text NOT NULL CHECK (source IN ('setup','model','user')),
    -- Until this is true the alias does not scope anything. A model proposal that nobody has
    -- looked at must never silently decide whose premium you are being shown: an unconfirmed
    -- alias is a question on Today, not an answer. `core/household.py` enforces it in one
    -- place -- `resolve_owner_aliases` filters on it -- and this column is what it reads.
    confirmed  boolean NOT NULL DEFAULT false,
    -- The generator's own confidence in a `model` proposal. Null for setup and user. Kept for
    -- the same reason facts.confidence is: it is how we find out whether the model is worth
    -- believing, and it is the column the threshold gets tuned against later.
    confidence real,
    -- The document that prompted the question, so the screen asking it can show the page.
    -- Null for aliases nobody needed a document to decide.
    document_id uuid REFERENCES documents(id) ON DELETE SET NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    decided_at timestamptz
);

-- One alias string resolves to one person, and the comparison is the one the resolver does.
CREATE UNIQUE INDEX person_aliases_unique ON person_aliases (lower(btrim(alias)));
CREATE INDEX person_aliases_person ON person_aliases (person_id, confirmed);
-- The query the "who is this?" row on Today runs.
CREATE INDEX person_aliases_pending ON person_aliases (created_at) WHERE NOT confirmed;

-- Which Telegram chat belongs to which person.
--
-- The bot already allowlists chat ids; this says whose each one is. It matters because it is
-- the only signal about ownership that arrives BEFORE the document is parsed: a photograph of
-- a payslip sent from Rachel's phone is Rachel's payslip, whatever the OCR makes of the name
-- at the top. `scripts/telegram_bot.py` stamps it; extraction may still disagree, and when it
-- does the disagreement is a question on Today rather than a silent overwrite.
CREATE TABLE telegram_identities (
    chat_id    bigint PRIMARY KEY,
    person_id  bigint NOT NULL REFERENCES people(id) ON DELETE CASCADE,
    created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX telegram_identities_person ON telegram_identities (person_id);

-- Which person a captured document was attributed to at capture time, and how.
--
-- Separate from `facts.subject` on purpose. A fact's subject is a claim the *page* makes; this
-- is a claim the *channel* makes. Keeping them apart is what lets Parrot say "this arrived
-- from Rachel's phone but the name on it is Marcus" instead of having to pick one and lose the
-- other.
CREATE TABLE document_attribution (
    document_id uuid PRIMARY KEY REFERENCES documents(id) ON DELETE CASCADE,
    person_id   bigint NOT NULL REFERENCES people(id) ON DELETE CASCADE,
    -- telegram = the chat it arrived on; user = somebody said so on a screen.
    source      text NOT NULL CHECK (source IN ('telegram','user')),
    created_at  timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX document_attribution_person ON document_attribution (person_id);
