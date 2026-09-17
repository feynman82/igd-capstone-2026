"""The register is the evaluation ground truth. These are the checks that keep it honest."""

from pathlib import Path

from corpus.validate import validate

# One column per field, which is what `python -m packs.build` writes into
# corpus/register/core_columns.csv. A test that used a hand-written header would not notice
# the generator and the validator drifting apart, which is the failure these tests exist for.
HEADER = (
    "doc_id,doc_type,pack_id,issued_date,subject,tier,"
    "insurer,policy_no,insured,cover_from,expiry_date,premium_payable,"
    "gross_salary,net_pay,field_pages,notes\n"
)


def _write(tmp_path: Path, *rows: str) -> Path:
    p = tmp_path / "reg.csv"
    p.write_text(HEADER + "".join(r + "\n" for r in rows), encoding="utf-8")
    return p


def test_template_register_is_clean() -> None:
    assert validate(Path("corpus/register/register.template.csv")) == []


def test_the_generated_header_is_the_one_the_validator_reads() -> None:
    """The contract between `packs.build` and this validator, asserted rather than assumed.

    Every column the generator emits must be one the validator accepts. When these two drifted
    apart, a correctly filled register was rejected as carrying no ground truth.
    """
    for generated in Path("corpus/register").glob("*_columns.csv"):
        header = next(
            line for line in generated.read_text(encoding="utf-8").splitlines() if line[:1] != "#"
        )
        row = header.split(",")
        body = ",".join("" for _ in row)
        sample = generated.parent / "sample.csv"
        try:
            sample.write_text(f"{header}\n{body}\n", encoding="utf-8")
            problems = validate(sample)
        finally:
            sample.unlink(missing_ok=True)
        assert not any("is not a field core/documents.yaml declares" in p for p in problems), (
            f"{generated.name} emits a column the validator rejects: {problems}"
        )


def test_the_batch_template_is_usable_exactly_as_generated(tmp_path: Path) -> None:
    """Copy it, fill rows under the guide block, validate. That is the whole handover path.

    The guide block is `#` lines, and `csv.DictReader` would otherwise read the first of them
    as the header row — which turned a correctly filled register into 122 errors, none of
    which named the real problem.
    """
    template = Path("corpus/register/batch.template.csv")
    lines = template.read_text(encoding="utf-8").splitlines()
    header = next(line for line in lines if not line.startswith("#"))
    columns = header.split(",")

    def row(**values: str) -> str:
        return ",".join(values.get(column, "") for column in columns)

    filled = tmp_path / "batch1.csv"
    filled.write_text(
        "\n".join(
            [
                *lines,
                row(
                    doc_id="b1-0001",
                    doc_type="payslip",
                    pack_id="core",
                    issued_date="2026-01-25",
                    subject="Marcus Fernandez",
                    tier="clean",
                    employee="Marcus Fernandez",
                    employer="Harborline Logistics Pte Ltd",
                    pay_period="2026-01",
                    gross_salary="8900.00",
                    net_pay="7120.00",
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    assert validate(filled) == []


def test_a_batch_mixes_packs_in_one_register(tmp_path: Path) -> None:
    """A batch is a household's documents, not one pack's, so the template spans both."""
    header = next(
        line
        for line in Path("corpus/register/batch.template.csv")
        .read_text(encoding="utf-8")
        .splitlines()
        if not line.startswith("#")
    ).split(",")
    assert "premium_payable" in header, "insurance fields missing from the batch template"
    assert "gross_salary" in header, "tax fields missing from the batch template"
    assert "field_pages" in header


def test_expiry_before_start_is_caught(tmp_path: Path) -> None:
    p = _write(
        tmp_path,
        "b1-1,policy_schedule,core,2026-03-01,SJ1,clean,,,,2026-03-01,2026-02-01,,,,,",
    )
    assert any("expiry_date" in e for e in validate(p))


def test_the_same_policy_must_look_identical_everywhere(tmp_path: Path) -> None:
    p = _write(
        tmp_path,
        "b1-1,policy_schedule,core,2026-03-01,SJ1,clean,Meridian Assurance,MV-1,,,,,,,,",
        "b1-2,renewal_notice,core,2027-01-01,SJ1,clean,Straits Mutual,MV-1,,,,,,,,",
    )
    assert any("differs across documents" in e for e in validate(p))


def test_a_row_with_no_fields_carries_no_ground_truth(tmp_path: Path) -> None:
    p = _write(tmp_path, "b1-1,payslip,core,2026-01-25,adult_1,clean,,,,,,,,,,")
    assert any("no fields" in e for e in validate(p))


def test_duplicate_ids_are_caught(tmp_path: Path) -> None:
    row = "b1-1,payslip,core,2026-01-25,adult_1,clean,,,,,,,8900,7120,,"
    assert any("duplicate" in e for e in validate(_write(tmp_path, row, row)))


def test_the_superseded_wide_format_is_named_rather_than_read_as_empty(tmp_path: Path) -> None:
    """A register in the old shape is full of ground truth, so "no fields" would be a lie."""
    p = tmp_path / "old.csv"
    p.write_text(
        "doc_id,doc_type,pack_id,issued_date,subject,tier,"
        "field_1_name,field_1_value,notes\n"
        "b1-1,payslip,core,2026-01-25,adult_1,clean,gross_salary,8900,\n",
        encoding="utf-8",
    )
    problems = validate(p)
    assert any("superseded" in e for e in problems)
    assert not any("no ground truth" in e for e in problems)


def test_a_header_without_field_pages_is_caught(tmp_path: Path) -> None:
    """Without it a golden-set question cannot say which page its answer is printed on."""
    p = tmp_path / "nopages.csv"
    p.write_text(
        "doc_id,doc_type,pack_id,issued_date,subject,tier,gross_salary,net_pay,notes\n"
        "b1-1,payslip,core,2026-01-25,adult_1,clean,8900,7120,\n",
        encoding="utf-8",
    )
    assert any("field_pages" in e for e in validate(p))


def test_field_pages_records_the_page_a_value_is_printed_on(tmp_path: Path) -> None:
    p = _write(
        tmp_path,
        "b1-1,policy_schedule,core,2026-03-01,SJ1,clean,"
        "Meridian Assurance,MV-1,,2026-03-01,2027-02-28,742.00,,,premium_payable=2,",
    )
    assert validate(p) == []


def test_field_pages_naming_a_field_the_row_does_not_fill_is_caught(tmp_path: Path) -> None:
    """Otherwise the golden question cites a page for a value that is not in the register."""
    p = _write(
        tmp_path,
        "b1-1,policy_schedule,core,2026-03-01,SJ1,clean,Meridian Assurance,MV-1,,,,,,,excess=2,",
    )
    assert any("does not fill" in e for e in validate(p))


def test_an_unparseable_page_is_caught(tmp_path: Path) -> None:
    p = _write(
        tmp_path,
        "b1-1,policy_schedule,core,2026-03-01,SJ1,clean,"
        "Meridian Assurance,MV-1,,,,,,,premium_payable=front,",
    )
    assert any("whole number" in e for e in validate(p))


def test_page_zero_is_caught(tmp_path: Path) -> None:
    """Pages are 1-based because that is how a person reads a citation off a chip."""
    p = _write(
        tmp_path,
        "b1-1,policy_schedule,core,2026-03-01,SJ1,clean,"
        "Meridian Assurance,MV-1,,,,742.00,,,premium_payable=0,",
    )
    assert any("1 or greater" in e for e in validate(p))
