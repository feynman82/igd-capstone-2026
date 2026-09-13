"""Restart and shut down: asked for by the screens, carried out by the supervisor.

The engine cannot restart itself in place. A restart that keeps the same interpreter keeps every
module it has already imported, so a fix on disk would not be running after the button said it
was. So the engine only ever *asks*: it records what was requested and tells uvicorn to exit, and
`scripts/run_parrot.py` decides what that exit means by its code — `RESTART_EXIT_CODE` starts a
fresh engine, anything else stops.

This lives in `core/runtime/` rather than in `api/` or `scripts/` because both of those need it
and neither may import the other.
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from typing import Literal

Action = Literal["restart", "shutdown"]
ACTIONS: tuple[Action, ...] = ("restart", "shutdown")

# EX_TEMPFAIL from sysexits.h, "try again later". Nothing else in this stack exits with it, which
# is what lets the supervisor tell a requested restart from a crash — and a crash is never retried.
RESTART_EXIT_CODE = 75


class Lifecycle:
    """What the person asked for, once. The first request wins; later ones change nothing."""

    def __init__(self, request_exit: Callable[[], None]) -> None:
        self._request_exit = request_exit
        self._lock = threading.Lock()
        self.requested: Action | None = None

    def request(self, action: Action) -> None:
        with self._lock:
            if self.requested is not None:
                return
            self.requested = action
        self._request_exit()

    def exit_code(self, *, started: bool) -> int:
        if self.requested == "restart":
            return RESTART_EXIT_CODE
        return 0 if started else 1
