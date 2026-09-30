"""How a question about a printed field is worded, per document type in `core/documents.yaml`.

Two wordings for every field, and the pair is the point. One names the thing as it is *printed*
— `policy MV-2026-448120`, `claim CLM-2026-0041` — and one names it as a person would say it —
`the Private Car Insurance Policy`, `Marcus's claim letter`. Exact identifiers are what hybrid
search's lexical arm exists to find and what dense search alone misses; paraphrase is what dense
search is for. A golden set carrying only one of the two measures only half the retriever.

This table is the part a generator cannot infer. The catalogue says a `policy_schedule` has an
`excess`; only a person knows that the question is "What is the excess on …?" and not "What is
the excess of …?". Each lane is free to rewrite its own wordings — these exist so that a lane
starts from twelve gradeable questions rather than a blank file.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

Row = Mapping[str, str]


@dataclass(frozen=True, slots=True)
class TypeSpec:
    """One document type's wordings.

    `printed` and `spoken` each render the *thing* a question is about, and every question in
    `asks` is that thing dropped into one template. A field used to build a wording is not asked
    about in that wording — "What is the policy number of policy MV-2026-448120?" answers itself.
    """

    label: str  # "policy schedule", as a person would name the document
    asks: Mapping[str, str]  # field -> a question with one {thing}
    printed: str = ""  # "policy {policy_no}" — the reference as the document prints it
    spoken: str = ""  # "the {product_name}" — how a person refers to it

    def thing(self, row: Row, template: str) -> str | None:
        """A wording, or `None` when the row does not fill every field it needs."""
        if not template:
            return None
        try:
            values = {key: (row.get(key) or "").strip() for key in _keys(template)}
        except KeyError:
            return None
        if not all(values.values()):
            return None
        return template.format(**values)

    def spoken_or_subject(self, row: Row) -> str | None:
        """The spoken wording, or "Rachel's payslip" when the type has no product name of its
        own. A document with neither is not asked about in the spoken form."""
        wording = self.thing(row, self.spoken)
        if wording:
            return wording
        subject = (row.get("subject") or "").strip()
        return f"{subject}'s {self.label}" if subject else None

    def question(self, row: Row, key: str, form: str) -> str | None:
        template = self.asks.get(key)
        if template is None:
            return None
        wording = (
            self.thing(row, self.printed) if form == "printed" else self.spoken_or_subject(row)
        )
        return None if wording is None else template.format(thing=wording)


def _keys(template: str) -> frozenset[str]:
    """The field names a template interpolates. `{thing}` is the question's own slot."""
    import string

    return frozenset(
        name for _, name, _, _ in string.Formatter().parse(template) if name and name != "thing"
    )


def _spec(label: str, asks: dict[str, str], printed: str = "", spoken: str = "") -> TypeSpec:
    return TypeSpec(label=label, asks=asks, printed=printed, spoken=spoken)


# A `repeats` field prints one labelled amount per row ("Waiver=120.00;Early CI=50000.00"), so
# there is no single value an answer can be checked against. Those are left to a person.
SPECS: dict[str, TypeSpec] = {
    "policy_schedule": _spec(
        "policy schedule",
        printed="policy {policy_no}",
        spoken="the {product_name}",
        asks={
            "insurer": "Which insurer issued {thing}?",
            "policy_no": "What is the policy number of {thing}?",
            "insured": "Who is the insured on {thing}?",
            "product_name": "What product is {thing}?",
            "cover_from": "When does cover under {thing} start?",
            "expiry_date": "When does {thing} expire?",
            "maturity_date": "When does {thing} mature?",
            "premium_payable": "What is the premium on {thing}?",
            "sum_insured": "What is the sum insured under {thing}?",
            "excess": "What is the excess on {thing}?",
            "date_of_birth": "What date of birth is printed on {thing}?",
        },
    ),
    "renewal_notice": _spec(
        "renewal notice",
        printed="the renewal notice for policy {policy_no}",
        asks={
            "insurer": "Which insurer sent {thing}?",
            "policy_no": "Which policy does {thing} renew?",
            "insured": "Who is {thing} addressed to?",
            "expiry_date": "When does the cover named on {thing} end?",
            "renewal_premium": "What is the renewal premium on {thing}?",
            "payment_due_date": "By when must {thing} be paid?",
        },
    ),
    "claim_letter": _spec(
        "claim letter",
        printed="claim {claim_no}",
        asks={
            "insurer": "Which insurer wrote about {thing}?",
            "policy_no": "Which policy was {thing} made against?",
            "claim_no": "What is the claim reference on {thing}?",
            "claimant": "Who is {thing} about?",
            "incident_date": "When did the incident behind {thing} happen?",
            "settled_amount": "How much was settled on {thing}?",
        },
    ),
    "benefit_illustration": _spec(
        "benefit illustration",
        printed="the illustration for policy {policy_no}",
        asks={
            "insurer": "Which insurer issued {thing}?",
            "policy_no": "Which policy does {thing} illustrate?",
            "life_assured": "Who is the life assured on {thing}?",
            "sum_assured": "What is the sum assured on {thing}?",
            "annual_premium": "What is the annual premium on {thing}?",
        },
    ),
    "policy_anniversary_statement": _spec(
        "policy anniversary statement",
        printed="the anniversary statement for policy {policy_no}",
        asks={
            "insurer": "Which insurer issued {thing}?",
            "policy_no": "Which policy is {thing} for?",
            "life_assured": "Who is the life assured on {thing}?",
            "statement_date": "What date is {thing} made up to?",
            "sum_assured": "What is the sum assured on {thing}?",
            "annual_premium": "What is the annual premium on {thing}?",
            "surrender_value": "What is the surrender value on {thing}?",
            "premiums_paid_to_date": "How much has been paid in premiums on {thing}?",
        },
    ),
    "payslip": _spec(
        "payslip",
        printed="the payslip for {pay_period}",
        asks={
            "employee": "Who is {thing} for?",
            "employer": "Which employer issued {thing}?",
            "pay_period": "Which month does {thing} cover?",
            "gross_salary": "What is the gross pay on {thing}?",
            "cpf_employee": "How much CPF was deducted on {thing}?",
            "net_pay": "What is the net pay on {thing}?",
        },
    ),
    "donation_receipt": _spec(
        "donation receipt",
        printed="receipt {receipt_no}",
        asks={
            "donor": "Who made the donation on {thing}?",
            "charity": "Which charity issued {thing}?",
            "receipt_no": "What is the receipt number on {thing}?",
            "donation_date": "When was the donation on {thing} made?",
            "donation_amount": "How much was donated on {thing}?",
            "tax_deductible": "Is the donation on {thing} tax deductible?",
        },
    ),
    "cpf_statement": _spec(
        "CPF statement",
        printed="the {statement_year} CPF statement",
        asks={
            "member": "Whose CPF account does {thing} report?",
            "statement_year": "Which year does {thing} cover?",
            "total_contributions": "What were the total contributions on {thing}?",
            "ordinary_account_balance": "What is the Ordinary Account balance on {thing}?",
        },
    ),
    "srs_statement": _spec(
        "SRS statement",
        printed="SRS account {account_no}",
        asks={
            "account_holder": "Who is {thing} issued to?",
            "account_no": "What is the account number on {thing}?",
            "statement_year": "Which year does {thing} cover?",
            "contributions_ytd": "What are the contributions to date on {thing}?",
        },
    ),
    "notice_of_assessment": _spec(
        "notice of assessment",
        printed="the notice of assessment for {assessment_year}",
        asks={
            "taxpayer": "Who is {thing} addressed to?",
            "assessment_year": "Which year of assessment is {thing} for?",
            "assessable_income": "What is the assessable income on {thing}?",
            "tax_payable": "How much tax is payable on {thing}?",
            "payment_due_date": "By when must the tax on {thing} be paid?",
        },
    ),
    # Identity documents carry the number a person would rather not type, so they are asked
    # about by whose they are. The printed wording is left empty on purpose.
    "identity_card": _spec(
        "identity card",
        asks={
            "id_number": "What is the identity card number on {thing}?",
            "full_name": "What name is printed on {thing}?",
            "date_of_birth": "What date of birth is on {thing}?",
        },
    ),
    "passport": _spec(
        "passport",
        asks={
            "passport_no": "What is the passport number on {thing}?",
            "full_name": "What name is printed on {thing}?",
            "date_of_birth": "What date of birth is on {thing}?",
            "date_of_expiry": "When does {thing} expire?",
        },
    ),
    "birth_certificate": _spec(
        "birth certificate",
        asks={
            "registration_no": "What is the registration number on {thing}?",
            "child_name": "Whose birth does {thing} record?",
            "date_of_birth": "What date of birth is on {thing}?",
        },
    ),
    "loan_agreement": _spec(
        "loan agreement",
        printed="facility {facility_no}",
        spoken="the loan from {lender}",
        asks={
            "lender": "Who is the lender on {thing}?",
            "facility_no": "What is the facility number on {thing}?",
            "borrower": "Who is the borrower on {thing}?",
            "principal": "What is the principal on {thing}?",
            "monthly_repayment": "What is the monthly repayment on {thing}?",
            "agreement_date": "When was {thing} agreed?",
        },
    ),
}


@dataclass(frozen=True, slots=True)
class LaneSpec:
    """Which register rows a lane's questions are drawn from.

    The task asks each member for twelve questions about the thing their lane built, so the
    split is by document type — except Lane E, whose subject is the scan and the photograph
    rather than any one type, and which therefore takes the degraded tiers of all of them.
    """

    owner: str
    why: str
    types: tuple[str, ...] = ()  # empty means any type
    tiers: tuple[str, ...] = ()  # empty means any tier
    excludes: tuple[str, ...] = ()  # types this lane leaves to another


def lane_of(row: Mapping[str, str]) -> str | None:
    """The one lane a register row belongs to, or `None` when no lane claims it.

    Exactly one, because two lanes drawing on one row would write the same question into two
    files under the same id. The first match in `LANES` order wins, and the order is the reason
    each lane's entry says what it leaves to another.
    """
    for lane, spec in LANES.items():
        doc_type, tier = row.get("doc_type") or "", row.get("tier") or ""
        if doc_type in spec.excludes:
            continue
        if (not spec.types or doc_type in spec.types) and (not spec.tiers or tier in spec.tiers):
            return lane
    return None


# Order matters: `lane_of` gives a row to the first lane that claims it. Lane E is first
# because its subject is the scan and the photograph rather than any one document type — a
# photographed claim letter is Desmond's question, not Zee's. The identity documents are the
# exception: they exist only as photographs, and ADR 0017 gave them to the core, so they stay
# with the lane that owns the household rather than with the lane that owns degraded scans.
LANES: dict[str, LaneSpec] = {
    "corpus": LaneSpec(
        "Desmond (E)",
        "the scanned and photographed tiers, whatever the document type",
        tiers=("scanned", "photo"),
        excludes=("identity_card", "passport", "birth_certificate"),
    ),
    "integration": LaneSpec(
        "Christian (A)",
        "identity, dates of birth and loans — the household data ADR 0017 gave the core",
        types=("identity_card", "passport", "birth_certificate", "loan_agreement"),
    ),
    "retrieval": LaneSpec(
        "Yew Mun (B)",
        "policy schedules: the exact identifiers hybrid search is for, and their paraphrases",
        types=("policy_schedule",),
    ),
    "packs": LaneSpec(
        "Zee (D)",
        "the documents the insurance pack speaks for beyond the schedule",
        types=(
            "renewal_notice",
            "claim_letter",
            "benefit_illustration",
            "policy_anniversary_statement",
        ),
    ),
    "governance": LaneSpec(
        "Siew (C)",
        "pay, CPF, SRS, tax and donations: the money documents an answer must be careful with",
        types=(
            "payslip",
            "cpf_statement",
            "srs_statement",
            "notice_of_assessment",
            "donation_receipt",
        ),
    ),
}
