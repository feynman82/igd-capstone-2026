"""The register is the evaluation ground truth. These are the checks that keep it honest."""

from pathlib import Path

from corpus.validate import validate

HEADER = (
    "doc_id,doc_type,pack_id,issued_date,subject,tier,"
    "field_1_name,field_1_value,field_2_name,field_2_value,notes\n"
)


def _write(tmp_path: Path, *rows: str) -> Path:
    p = tmp_path / "reg.csv"
    p.write_text(HEADER + "".join(r + "\n" for r in rows), encoding="utf-8")
    return p


def test_template_register_is_clean() -> None:
    assert validate(Path("corpus/register/register.template.csv")) == []


def test_expiry_before_start_is_caught(tmp_path: Path) -> None:
    p = _write(
        tmp_path,
        "b1-1,policy_schedule,insurance_agent,2026-03-01,SJ1,clean,"
        "cover_from,2026-03-01,expiry_date,2026-02-01,",
    )
    assert any("expiry_date" in e for e in validate(p))


def test_the_same_policy_must_look_identical_everywhere(tmp_path: Path) -> None:
    p = _write(
        tmp_path,
        "b1-1,policy_schedule,insurance_agent,2026-03-01,SJ1,clean,"
        "policy_no,MV-1,insurer,Meridian Assurance,",
        "b1-2,renewal_notice,insurance_agent,2027-01-01,SJ1,clean,"
        "policy_no,MV-1,insurer,Straits Mutual,",
    )
    assert any("differs across documents" in e for e in validate(p))


def test_a_row_with_no_fields_carries_no_ground_truth(tmp_path: Path) -> None:
    p = _write(tmp_path, "b1-1,payslip,iras_tax,2026-01-25,adult_1,clean,,,,,")
    assert any("no fields" in e for e in validate(p))


def test_duplicate_ids_are_caught(tmp_path: Path) -> None:
    row = "b1-1,payslip,iras_tax,2026-01-25,adult_1,clean,gross_salary,8900,net_pay,7120,"
    assert any("duplicate" in e for e in validate(_write(tmp_path, row, row)))
