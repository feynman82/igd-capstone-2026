"""The ingestion worker.

Capture registers a document; this package turns it into chunks for retrieval and facts for
the modules, in one transaction, or puts it in quarantine with a reason. See
`core/ingest/README.md`.
"""

from core.ingest.pipeline import Outcome, process
from core.ingest.register import Registrar, Registration, register_document

__all__ = ["Outcome", "Registrar", "Registration", "process", "register_document"]
