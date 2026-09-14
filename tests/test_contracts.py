"""The contracts are the platform. If these break, something important changed."""

import copy
from collections.abc import Callable
from pathlib import Path
from typing import Any, get_args

import pytest
import yaml
from pydantic import ValidationError

import core.contracts as contracts
import core.packs as loader
from core.contracts import GroundingCorpus, ModuleManifest, PackManifest
from core.packs import InstalledPack, PackUnavailable


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


def _tax() -> dict[str, Any]:
    with open("packs/iras_tax/pack.yaml", encoding="utf-8") as fh:
        raw: dict[str, Any] = yaml.safe_load(fh)
    return raw


def test_a_pack_cannot_opt_out_of_verdict_by_code() -> None:
    raw = _insurance()
    raw["guardrails"]["verdict_by_code"] = False
    with pytest.raises(ValidationError) as caught:
        PackManifest.model_validate(raw)
    # The type refuses it, not `extra="forbid"`: an unknown key would fail for the wrong reason.
    assert [error["type"] for error in caught.value.errors()] == ["literal_error"]


# ---------------------------------------------------------------------------- advice


def _advised() -> dict[str, Any]:
    """The insurance pack plus one rule key, a critical illness gap and a hospital plan comparison.

    Built here and not in pack.yaml: the advice wording in a real pack is Zee's, reviewed by Siew.
    """
    raw = _insurance()
    raw["grounding"] = {
        "corpus": None,
        "top_k": 0,
        "values": [
            {
                "key": "ci_multiple",
                "unit": "multiple",
                "description": "Multiple of annual income a household is guided to hold as cover",
                "qualifiers": ["age_band"],
            }
        ],
    }
    raw["advice"] = {
        "consent_version": "1.0.0",
        "consent_text": (
            "I agree that Parrot may calculate advice from my household's documents and the "
            "published guidance it holds."
        ),
        "disclaimer": (
            "A calculation from your own documents and published guidance, not a recommendation "
            "from a licensed adviser."
        ),
        "product_disclosure": (
            "Where a product is named, only what both documents print is compared."
        ),
        "shapes": [
            {
                "id": "ci_gap",
                "calculator": "gap",
                "label": "critical illness cover gap",
                "asked": ["enough critical illness", "critical illness gap"],
                "facts": [
                    {
                        "role": "income",
                        "pack": "iras_tax",
                        "doc_types": ["payslip"],
                        "field": "gross_salary",
                        "per": "month",
                        "missing": "A recent payslip, to know your income.",
                    },
                    {
                        "role": "held",
                        "doc_types": ["policy_schedule"],
                        "field": "sum_insured",
                        "category": "critical_illness",
                        "take": "sum",
                        "missing": "The schedule of each critical illness plan you hold.",
                    },
                ],
                "rules": [
                    {
                        "role": "multiple",
                        "key": "ci_multiple",
                        "missing": "Reviewed guidance on how much cover to hold.",
                    }
                ],
                "never_say": ["you must buy"],
            },
            {
                "id": "hospital_plans",
                "calculator": "compare_own",
                "label": "hospital plans compared",
                "asked": ["which hospital plan"],
                "facts": [
                    {
                        "role": "items",
                        "doc_types": ["policy_schedule"],
                        "field": "premium_payable",
                        "category": "hospital_expense",
                        "take": "each",
                        "missing": "The schedule of each hospital plan you hold.",
                    }
                ],
                "compare_fields": ["premium_payable", "excess"],
                "order_by": "premium_payable",
                "disadvantages": ["A lower premium can come with a higher excess."],
            },
        ],
    }
    return raw


def _shape(raw: dict[str, Any], shape_id: str) -> dict[str, Any]:
    shape: dict[str, Any] = next(s for s in raw["advice"]["shapes"] if s["id"] == shape_id)
    return shape


def _fact(raw: dict[str, Any], shape_id: str, role: str) -> dict[str, Any]:
    fact: dict[str, Any] = next(f for f in _shape(raw, shape_id)["facts"] if f["role"] == role)
    return fact


def test_an_insurance_manifest_with_advice_validates() -> None:
    manifest = PackManifest.model_validate(_advised())
    assert manifest.advice is not None
    assert [shape.id for shape in manifest.advice.shapes] == ["ci_gap", "hospital_plans"]
    income, held = manifest.advice.shapes[0].facts
    assert (income.pack, income.per, income.take) == ("iras_tax", "month", "latest")
    assert (held.pack, held.category, held.take) == (None, "critical_illness", "sum")
    assert [value.key for value in manifest.grounding.values] == ["ci_multiple"]
    assert manifest.guardrails.verdict_by_code is True


def test_every_calculator_declares_the_roles_it_reads() -> None:
    assert set(contracts.CALCULATOR_ROLES) == set(get_args(contracts.AdviceCalculator))


def _drop_held(raw: dict[str, Any]) -> None:
    shape = _shape(raw, "ci_gap")
    shape["facts"] = [f for f in shape["facts"] if f["role"] != "held"]


def _drop_rules(raw: dict[str, Any]) -> None:
    _shape(raw, "ci_gap")["rules"] = []


def _undeclared_doc_type(raw: dict[str, Any]) -> None:
    _fact(raw, "ci_gap", "held")["doc_types"] = ["not_a_doc"]


def _field_not_on_every_doc_type(raw: dict[str, Any]) -> None:
    _fact(raw, "ci_gap", "held")["doc_types"] = ["policy_schedule", "renewal_notice"]


def _undeclared_category(raw: dict[str, Any]) -> None:
    _fact(raw, "ci_gap", "held")["category"] = "not_a_category"


def _undeclared_rule_key(raw: dict[str, Any]) -> None:
    _shape(raw, "ci_gap")["rules"][0]["key"] = "not_a_key"


def _order_by_not_compared(raw: dict[str, Any]) -> None:
    _shape(raw, "hospital_plans")["order_by"] = "sum_insured"


def _compare_without_an_ordering(raw: dict[str, Any]) -> None:
    shape = _shape(raw, "hospital_plans")
    shape["compare_fields"] = []
    shape["order_by"] = None


def _duplicate_shape(raw: dict[str, Any]) -> None:
    raw["advice"]["shapes"].append(copy.deepcopy(_shape(raw, "ci_gap")))


@pytest.mark.parametrize(
    ("mutate", "names"),
    [
        (_drop_held, "ci_gap.*held"),
        (_drop_rules, "ci_gap.*multiple"),
        (_undeclared_doc_type, "ci_gap.*not_a_doc"),
        (_field_not_on_every_doc_type, "ci_gap.*sum_insured.*renewal_notice"),
        (_undeclared_category, "ci_gap.*not_a_category"),
        (_undeclared_rule_key, "ci_gap.*not_a_key"),
        (_order_by_not_compared, "hospital_plans.*sum_insured"),
        (_compare_without_an_ordering, "hospital_plans"),
        (_duplicate_shape, "duplicate.*ci_gap"),
    ],
    ids=lambda value: value.__name__.lstrip("_") if callable(value) else None,
)
def test_an_inconsistent_advice_block_is_rejected_by_name(
    mutate: Callable[[dict[str, Any]], None], names: str
) -> None:
    raw = _advised()
    mutate(raw)
    with pytest.raises(ValidationError, match=names):
        PackManifest.model_validate(raw)


def _installed(raw: dict[str, Any]) -> InstalledPack:
    return InstalledPack(PackManifest.model_validate(raw), {}, {})


def test_advice_reading_an_uninstalled_pack_is_rejected() -> None:
    with pytest.raises(PackUnavailable, match=r"ci_gap.*iras_tax"):
        loader.check_advice_links([_installed(_advised())])


def test_advice_reading_an_undeclared_field_of_an_installed_pack_is_rejected() -> None:
    raw = _advised()
    _fact(raw, "ci_gap", "income")["field"] = "not_a_field"
    with pytest.raises(PackUnavailable, match=r"ci_gap.*not_a_field"):
        loader.check_advice_links([_installed(raw), _installed(_tax())])


def test_advice_reading_a_declared_field_of_an_installed_pack_links() -> None:
    loader.check_advice_links([_installed(_advised()), _installed(_tax())])


def test_a_module_may_read_grounding_values() -> None:
    manifest = ModuleManifest.model_validate(
        {
            "id": "tracker",
            "version": "0.1.0",
            "reads": ["facts", "grounding_values"],
            "writes": [],
            "runs": {"on": "fact_write"},
            "surfaces": ["today"],
            "config_schema": "modules.tracker.Config",
        }
    )
    assert "grounding_values" in manifest.reads


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
    assert manifest.guardrails.verdict_by_code is True
    assert "recommend" in manifest.guardrails.advice_decline


def test_a_grounding_corpus_is_named_by_id_not_by_path() -> None:
    raw = _insurance()
    raw["grounding"] = {"corpus": "grounding/iras_reliefs_ya2026/", "top_k": 3}
    with pytest.raises(ValidationError):
        PackManifest.model_validate(raw)


_CORPORA = sorted(Path("packs").glob("*/grounding/*/sources.yaml"))


@pytest.mark.parametrize(
    "sources", _CORPORA, ids=lambda p: f"{p.parent.parent.parent.name}.{p.parent.name}"
)
def test_every_grounding_corpus_declares_its_provenance(sources: Path) -> None:
    corpus = GroundingCorpus.model_validate(yaml.safe_load(sources.read_text(encoding="utf-8")))
    assert corpus.corpus_id == sources.parent.name
    for document in corpus.documents:
        assert (sources.parent / document.file).is_file(), document.file


def test_a_grounding_corpus_travels_inside_its_pack() -> None:
    """A downloaded pack carries its sources, so no corpus is left at the repository root."""
    assert {p.parent.name for p in _CORPORA} >= {"iras_reliefs_ya2026", "mas_fair_dealing"}
    assert not list(Path("grounding").glob("*/sources.yaml"))
    for pack_yaml in sorted(Path("packs").glob("*/pack.yaml")):
        raw = yaml.safe_load(pack_yaml.read_text(encoding="utf-8"))
        corpus = PackManifest.model_validate(raw).grounding.corpus
        if corpus is not None:
            assert (pack_yaml.parent / "grounding" / corpus / "sources.yaml").is_file(), corpus


def test_every_installed_pack_still_loads() -> None:
    from core.packs import installed_packs

    installed_packs.cache_clear()
    assert {installed.id for installed in installed_packs()} >= {"insurance_agent", "iras_tax"}
