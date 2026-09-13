"""The contracts are the platform. If these break, something important changed."""

from pathlib import Path
from typing import Any

import pytest
import yaml
from pydantic import ValidationError

from core.contracts import GroundingCorpus, PackManifest


def test_template_pack_validates() -> None:
    with open("packs/_template/pack.yaml", encoding="utf-8") as fh:
        PackManifest.model_validate(yaml.safe_load(fh))


def test_a_pack_cannot_opt_out_of_never_acts() -> None:
    with open("packs/_template/pack.yaml", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)
    raw["guardrails"]["never_acts"] = False
    try:
        PackManifest.model_validate(raw)
    except Exception:
        return
    raise AssertionError("never_acts=False must be rejected by the type, not by review")


def test_generated_files_are_in_sync() -> None:
    """The register headers and the extraction models are generated from pack.yaml.

    If this fails, someone edited a pack and did not run `python -m packs.build`. That is
    exactly the drift this whole mechanism exists to prevent, so it is a hard failure.
    """
    import subprocess
    import sys

    r = subprocess.run(
        [sys.executable, "-m", "packs.build", "--check"], capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr


def _insurance() -> dict[str, Any]:
    with open("packs/insurance_agent/pack.yaml", encoding="utf-8") as fh:
        raw: dict[str, Any] = yaml.safe_load(fh)
    return raw


def test_a_pack_cannot_opt_out_of_never_recommends() -> None:
    raw = _insurance()
    raw["guardrails"]["never_recommends"] = False
    with pytest.raises(ValidationError):
        PackManifest.model_validate(raw)


def test_categories_must_read_a_field_the_pack_declares() -> None:
    raw = _insurance()
    raw["answering"] = {
        "categories": {
            "match_field": "not_a_field",
            "noun": "policies",
            "rules": [{"id": "dental", "label": "dental plan", "printed": ["dental"]}],
        }
    }
    with pytest.raises(ValidationError, match="not_a_field"):
        PackManifest.model_validate(raw)


def test_categories_reading_a_declared_field_validate() -> None:
    raw = _insurance()
    raw["answering"] = {
        "vocabulary": {"warded": "hospitalised as an inpatient"},
        "categories": {
            "match_field": "product_name",
            "noun": "policies",
            "rules": [{"id": "dental", "label": "dental plan", "printed": ["dental"]}],
        },
        "max_sentences": 6,
    }
    manifest = PackManifest.model_validate(raw)
    assert manifest.answering.categories is not None
    assert manifest.guardrails.never_recommends is True
    assert "recommend" in manifest.guardrails.advice_decline


def test_a_grounding_corpus_is_named_by_id_not_by_path() -> None:
    raw = _insurance()
    raw["grounding"] = {"corpus": "grounding/iras_reliefs_ya2026/", "top_k": 3}
    with pytest.raises(ValidationError):
        PackManifest.model_validate(raw)


@pytest.mark.parametrize(
    "sources", sorted(Path("grounding").glob("*/sources.yaml")), ids=lambda p: p.parent.name
)
def test_every_grounding_corpus_declares_its_provenance(sources: Path) -> None:
    corpus = GroundingCorpus.model_validate(yaml.safe_load(sources.read_text(encoding="utf-8")))
    assert corpus.corpus_id == sources.parent.name
    for document in corpus.documents:
        assert (sources.parent / document.file).is_file(), document.file


def test_every_installed_pack_still_loads() -> None:
    from core.packs import installed_packs

    installed_packs.cache_clear()
    assert {installed.id for installed in installed_packs()} >= {"insurance_agent", "iras_tax"}
