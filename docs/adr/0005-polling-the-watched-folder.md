# 5. The watched folder is polled for stability, not subscribed to for events

Date: 2026-09-11 · Status: accepted

## Context

`team/christian/README.md` describes the first capture adapter as a "watched folder
(debounced)", and `docs/team-tasks.csv` names the W2 task "Build the folder watchdog
adapter". The obvious reading is the `watchdog` package, which wraps each operating
system's native filesystem notification API.

Two things argue against reaching for it.

The first is that a filesystem event is the wrong signal. `watchdog` tells us a file was
created, and a file is created at the *start* of a copy, not at the end. A scanner writing
a 4 MB PDF, a phone syncing a photograph and a browser finishing a download all produce a
created-then-modified sequence with no event that means "finished". Anything built on
those events still has to debounce by watching the file stop changing, so the event stream
saves nothing — it only decides how often we look. On Windows, `ReadDirectoryChangesW`
additionally drops events under buffer pressure, which would mean a document silently
never filed.

The second is rule 5 in `AGENTS.md`: no new runtime dependency without an ADR. The
household inbox is one directory holding a handful of files a week. `Path.iterdir()` plus
`stat()` once a second is not a measurable cost on any machine this will run on.

## Decision

`core/adapters/folder.py` polls. A file is ready when its size and modification time have
been unchanged for `stable_seconds` (default 3.0) across polls `poll_seconds` apart
(default 1.0), and when it is not empty. That registers a document roughly four seconds
after a copy finishes — comfortably inside the sixty seconds the task requires — and never
reads a half-written file.

Time is passed into `FolderAdapter.observe(elapsed)` rather than read from a clock inside
it, so the debounce is tested without any test sleeping. `scripts/watch_folder.py` supplies
the real elapsed time.

Names that mean "still being written" are skipped outright: a leading `.` or `~$`, and the
suffixes `.part`, `.crdownload`, `.tmp`, `.download`, `.filepart`. Files larger than 64 MB
are skipped with a warning; a household document that large is a mistake rather than a scan.

No runtime dependency is added.

## Consequences

A document is filed within about four seconds rather than instantly. Nobody watching a
folder notices the difference, and the demonstration is not built on it.

The adapter holds its "already filed" memory in process, so restarting the watcher
re-reads files still sitting in the inbox. This costs one SHA-256 per file and produces no
duplicate rows — the upsert in `core/ingest/register.py` recognises the bytes and reports
"already filed" — but it does mean the log is noisier after a restart than during one.
Persisting that memory is not worth a table until the inbox is large enough to notice.

Directories are not recursed. A subfolder in the inbox is ignored, which is the behaviour a
person expects from a drop box and avoids filing an entire archive somebody unzipped there.

If a later channel genuinely needs sub-second capture, this decision is the one to revisit,
and `watchdog` with a stability check layered on top is what to revisit it with.
