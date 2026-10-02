"""The contracts are the platform. If these break, something important changed."""

import copy
from collections.abc import Callable
from pathlib import Path
from typing import Any, get_args

import pytest
import yaml
from pydantic import ValidationError

import core.contracts as contracts
from core.contracts import GroundingCorpus, ModuleManifest, PackManifest
from core.packs import catalog


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


def _checked(raw: dict[str, Any]) -> PackManifest:
    """Validated as a manifest, then against the core catalogue, as `core.packs` loads a pack."""
    manifest = PackManifest.model_validate(raw)
    manifest.check_against(catalog().documents)
    return manifest


def test_a_pack_declaring_document_types_is_rejected() -> None:
    """ADR 0017: documents are the core's. A pack.yaml carrying them does not load."""
    raw = _insurance()
    raw["document_types"] = copy.deepcopy(
        {"policy_schedule": catalog().documents.document_types["policy_schedule"].model_dump()}
    )
    with pytest.raises(ValidationError, match="document_types"):
        PackManifest.model_validate(raw)


def test_a_pack_declaring_registers_is_rejected() -> None:
    raw = _tax()
    raw["registers"] = {"reminder": [{"key": "filing_deadline", "lead_days": [30]}]}
    with pytest.raises(ValidationError, match="registers"):
        PackManifest.model_validate(raw)


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
    manifest = _checked(_advised())
    assert manifest.advice is not None
    assert [shape.id for shape in manifest.advice.shapes] == ["ci_gap", "hospital_plans"]
    income, held = manifest.advice.shapes[0].facts
    assert (income.doc_types, income.per, income.take) == (["payslip"], "month", "latest")
    assert (held.category, held.take) == ("critical_illness", "sum")
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


def _held_per_month(raw: dict[str, Any]) -> None:
    _fact(raw, "ci_gap", "held")["per"] = "month"


def _held_per_year(raw: dict[str, Any]) -> None:
    _fact(raw, "ci_gap", "held")["per"] = "year"


def _order_by_not_compared(raw: dict[str, Any]) -> None:
    _shape(raw, "hospital_plans")["order_by"] = "sum_insured"


def _compare_without_an_ordering(raw: dict[str, Any]) -> None:
    shape = _shape(raw, "hospital_plans")
    shape["compare_fields"] = []
    shape["order_by"] = None


def _duplicate_shape(raw: dict[str, Any]) -> None:
    raw["advice"]["shapes"].append(copy.deepcopy(_shape(raw, "ci_gap")))


def _compares_an_undeclared_field(raw: dict[str, Any]) -> None:
    _shape(raw, "hospital_plans")["compare_fields"] = ["premium_payable", "deductible"]


def _market(raw: dict[str, Any], compare_fields: list[str]) -> None:
    """A market comparison of the held hospital plan, on `compare_fields`, ordered by premium."""
    raw["grounding"]["values"].append(
        {
            "key": "annual_premium",
            "unit": "money",
            "description": "A published annual premium for a named plan and age band",
            "qualifiers": ["product", "insurer", "age_band"],
        }
    )
    raw["advice"]["shapes"].append(
        {
            "id": "hospital_market",
            "calculator": "compare_market",
            "label": "hospital plan against the market",
            "asked": ["better than an integrated shield"],
            "facts": [
                {
                    "role": "held",
                    "doc_types": ["policy_schedule"],
                    "field": "premium_payable",
                    "category": "hospital_expense",
                    "missing": "The schedule of the hospital plan you hold.",
                }
            ],
            "rules": [
                {
                    "role": "market",
                    "key": "annual_premium",
                    "missing": "Reviewed published premiums to compare against.",
                }
            ],
            "compare_fields": compare_fields,
            "order_by": compare_fields[0],
        }
    )


def _market_compares_an_undeclared_field(raw: dict[str, Any]) -> None:
    _market(raw, ["premium_payable", "ward_class"])


@pytest.mark.parametrize(
    ("mutate", "names"),
    [
        (_drop_held, "ci_gap.*held"),
        (_drop_rules, "ci_gap.*multiple"),
        (_undeclared_doc_type, "ci_gap.*not_a_doc"),
        (_field_not_on_every_doc_type, "ci_gap.*sum_insured.*renewal_notice"),
        (_undeclared_category, "ci_gap.*not_a_category"),
        (_undeclared_rule_key, "ci_gap.*not_a_key"),
        (_held_per_month, "advice shape 'ci_gap' reads 'held' per month, which only income may be"),
        (_held_per_year, "advice shape 'ci_gap' reads 'held' per year, which only income may be"),
        (_order_by_not_compared, "hospital_plans.*sum_insured"),
        (_compare_without_an_ordering, "hospital_plans"),
        (_duplicate_shape, "duplicate.*ci_gap"),
        (_compares_an_undeclared_field, "hospital_plans' compares 'deductible', which"),
        (_market_compares_an_undeclared_field, "hospital_market' compares 'ward_class', which"),
    ],
    ids=lambda value: value.__name__.lstrip("_") if callable(value) else None,
)
def test_an_inconsistent_advice_block_is_rejected_by_name(
    mutate: Callable[[dict[str, Any]], None], names: str
) -> None:
    raw = _advised()
    mutate(raw)
    with pytest.raises(ValueError, match=names):
        _checked(raw)


@pytest.mark.parametrize("per", ["once", "month", "year"])
def test_income_may_be_read_per_month_or_per_year(per: str) -> None:
    """Only income is made annual, so only income may say how often its printed figure recurs."""
    raw = _advised()
    _fact(raw, "ci_gap", "income")["per"] = per
    manifest = _checked(raw)
    assert manifest.advice is not None
    assert manifest.advice.shapes[0].facts[0].per == per


def test_a_market_comparison_may_compare_a_field_only_its_sources_publish() -> None:
    """`annual_premium` is printed on no policy schedule; the market's sources publish it."""
    raw = _advised()
    _market(raw, ["premium_payable", "annual_premium"])
    manifest = _checked(raw)
    assert manifest.advice is not None
    assert manifest.advice.shapes[-1].compare_fields == ["premium_payable", "annual_premium"]


def test_an_own_comparison_may_not_compare_a_field_only_sources_publish() -> None:
    """Two household documents can only be compared on what a household document prints."""
    raw = _advised()
    _market(raw, ["premium_payable"])
    _shape(raw, "hospital_plans")["compare_fields"] = ["premium_payable", "annual_premium"]
    with pytest.raises(ValueError, match="compares 'annual_premium', which"):
        _checked(raw)


def test_advice_naming_an_undeclared_catalogue_field_is_rejected_against_the_catalogue() -> None:
    """The manifest alone cannot know the catalogue, so it validates; `check_against` names it."""
    raw = _advised()
    _fact(raw, "ci_gap", "income")["field"] = "not_a_field"
    manifest = PackManifest.model_validate(raw)
    with pytest.raises(ValueError, match=r"insurance_agent: advice shape 'ci_gap'.*not_a_field"):
        manifest.check_against(catalog().documents)


def test_advice_naming_an_unknown_category_is_rejected_against_the_catalogue() -> None:
    raw = _advised()
    _fact(raw, "ci_gap", "held")["category"] = "not_a_category"
    manifest = PackManifest.model_validate(raw)
    with pytest.raises(ValueError, match=r"category 'not_a_category'"):
        manifest.check_against(catalog().documents)


def test_a_shape_closed_by_an_unknown_category_is_rejected() -> None:
    """`closed_by` names kinds of cover, so a typo would silently print nothing on a short
    verdict rather than fail — the gap would be stated with no way to close it."""
    raw = _advised()
    raw["advice"]["shapes"][0]["closed_by"] = ["spaceship"]
    manifest = PackManifest.model_validate(raw)
    with pytest.raises(ValueError, match=r"closed_by \['spaceship'\]"):
        manifest.check_against(catalog().documents)


def test_advice_reading_a_payslip_field_needs_no_second_pack() -> None:
    """ADR 0017: `FactInput.pack` is gone; a payslip's gross salary is a core fact."""
    assert "pack" not in contracts.FactInput.model_fields
    _checked(_advised())


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


def test_advice_is_a_module() -> None:
    """ADR 0016: calculators are a module, so `modules/advice/module.yaml` must load."""
    manifest = ModuleManifest.model_validate(
        {
            "id": "advice",
            "version": "1.0.0",
            "reads": ["facts", "grounding_values"],
            "writes": [],
            "runs": {"on": "fact_write"},
            "surfaces": ["chat_thread"],
            "config_schema": "core.contracts:AdviceShape",
        }
    )
    assert manifest.id == "advice"


def test_categories_must_read_a_field_the_pack_declares() -> None:
    raw = _insurance()
    raw["answering"] = {
        "categories": {
            "match_field": "not_a_field",
            "noun": "policies",
            "rules": [{"id": "dental", "label": "dental plan", "printed": ["dental"]}],
        }
    }
    with pytest.raises(ValueError, match="not_a_field"):
        _checked(raw)


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
    assert {p.parent.name for p in _CORPORA} >= {"iras_tax_ya2025_ya2027", "sg_protection_guidance"}
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


def test_a_pack_speaking_for_an_undeclared_type_is_rejected_at_load() -> None:
    raw = _tax()
    raw["answering"]["documents"] = ["payslip", "not_a_doc"]
    with pytest.raises(ValueError, match=r"iras_tax: answering.documents names 'not_a_doc'"):
        _checked(raw)


def test_every_pack_speaks_only_for_catalogue_types() -> None:
    from core.packs import installed_packs

    spoken = {t for p in installed_packs() for t in p.manifest.answering.documents}
    assert spoken <= set(catalog().documents.document_types)
    assert {"policy_schedule", "payslip"} <= spoken


def test_a_review_names_only_declared_shapes_and_categories() -> None:
    raw = _advised()
    raw["advice"]["review"] = {"label": "cover review", "asked": ["lacking"], "shapes": ["ci_gap"]}
    PackManifest.model_validate(raw)
    raw["advice"]["review"]["shapes"] = ["nope"]
    with pytest.raises(ValidationError, match="does not declare"):
        PackManifest.model_validate(raw)
    raw["advice"]["review"] = {
        "label": "cover review",
        "asked": ["lacking"],
        "shapes": ["ci_gap"],
        "holds": ["spaceship"],
    }
    with pytest.raises(ValueError, match="not category ids"):
        PackManifest.model_validate(raw).check_against(catalog().documents)


def test_a_review_is_explained_by_quotes_from_named_corpus_files() -> None:
    raw = _advised()
    step = {"file": "moneysense-guide.md", "quote": "This fact-finding process is called an FNA."}
    raw["advice"]["review"] = {
        "label": "cover review",
        "asked": ["lacking"],
        "shapes": ["ci_gap"],
        "explained_by": [step],
    }
    PackManifest.model_validate(raw)
    raw["advice"]["review"]["explained_by"] = [{**step, "file": "../outside.md"}]
    with pytest.raises(ValidationError):
        PackManifest.model_validate(raw)
