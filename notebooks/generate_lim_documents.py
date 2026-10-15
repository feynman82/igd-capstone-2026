"""
Project Parrot - Synthetic Document Generator for Lim Household
================================================================
Generates high-fidelity synthetic PDFs from HTML templates using Jinja2
and headless Edge/Chrome. All data is strictly consistent with corpus/canon.md.

Includes:
- Payslips (Marcus & Rachel)
- Life & Hospital Policy Schedules (Rachel, Lucas, Tan Mei Ling)
- Comprehensive Policy Contracts with surgical tables, heart stent coverage, kidney stones, and exclusions (Marcus & Dad)
- Residential Housing Loan Facility Letter (36-month lock-in, early sale penalties)
- Motor Vehicle Hire Purchase Agreement (Rule of 78, early settlement penalties)

Usage:
    python notebooks/generate_lim_documents.py [--output inbox/]
"""

import argparse
import subprocess
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = Path("corpus/templates")

DOCUMENTS = [
    {
        "doc_id": "b2-0001",
        "template": "payslip.html",
        "filename": "b2-0001_Rachel_Payslip_2026-07.pdf",
        "data": {
            "doc_id": "b2-0001",
            "employee": "Rachel Ng Hui Shan",
            "employer": "Northlight Health Pte Ltd",
            "pay_period": "2026-07",
            "gross_salary": "6250.00",
            "cpf_employee": "1250.00",
            "net_pay": "5000.00",
        },
    },
    {
        "doc_id": "b2-0002",
        "template": "payslip.html",
        "filename": "b2-0002_Marcus_Payslip_2026-06.pdf",
        "data": {
            "doc_id": "b2-0002",
            "employee": "Marcus Lim Jun Wei",
            "employer": "Meridian Systems Pte Ltd",
            "pay_period": "2026-06",
            "gross_salary": "9400.00",
            "cpf_employee": "1600.00",
            "net_pay": "7800.00",
        },
    },
    {
        "doc_id": "b2-0003",
        "template": "policy_schedule.html",
        "filename": "b2-0003_Rachel_TermLife_Schedule.pdf",
        "data": {
            "doc_id": "b2-0003",
            "insurer": "Lionhead Life Assurance",
            "policy_no": "LF-2024-883192",
            "insured": "Rachel Ng Hui Shan",
            "product_name": "LifeGuard Term Plan",
            "cover_from": "2024-10-01",
            "expiry_date": "2054-09-30",
            "premium_payable": "1420.00",
            "sum_insured": "500000.00",
            "excess": "Nil",
        },
    },
    {
        "doc_id": "b2-0004",
        "template": "policy_schedule.html",
        "filename": "b2-0004_Rachel_Hospital_Schedule.pdf",
        "data": {
            "doc_id": "b2-0004",
            "insurer": "Meridian Assurance",
            "policy_no": "PH-2024-912404",
            "insured": "Rachel Ng Hui Shan",
            "product_name": "PrivateCare Hospital and Surgical Plan",
            "cover_from": "2026-03-01",
            "expiry_date": "2027-02-28",
            "premium_payable": "1150.00",
            "sum_insured": "1000000.00",
            "excess": "3500.00",
        },
    },
    {
        "doc_id": "b2-0005",
        "template": "policy_schedule.html",
        "filename": "b2-0005_TanMeiLing_CareShield_Schedule.pdf",
        "data": {
            "doc_id": "b2-0005",
            "insurer": "Lionhead Life Assurance",
            "policy_no": "ES-2020-119284",
            "insured": "Tan Mei Ling",
            "product_name": "CareShield ElderPlus Plan",
            "cover_from": "2025-04-10",
            "expiry_date": "2031-04-09",
            "premium_payable": "890.00",
            "sum_insured": "72000.00",
            "excess": "Nil",
        },
    },
    {
        "doc_id": "b2-0006",
        "template": "policy_schedule.html",
        "filename": "b2-0006_Lucas_JuniorHealth_Schedule.pdf",
        "data": {
            "doc_id": "b2-0006",
            "insurer": "Meridian Assurance",
            "policy_no": "CH-2024-339102",
            "insured": "Lucas Lim Kai En",
            "product_name": "Junior HealthProtect Plan",
            "cover_from": "2024-08-01",
            "expiry_date": "2045-07-31",
            "premium_payable": "640.00",
            "sum_insured": "500000.00",
            "excess": "500.00",
        },
    },
    {
        "doc_id": "b2-0007",
        "template": "renewal_notice.html",
        "filename": "b2-0007_Rachel_Hospital_Renewal.pdf",
        "data": {
            "doc_id": "b2-0007",
            "insurer": "Meridian Assurance",
            "policy_no": "PH-2024-912404",
            "insured": "Rachel Ng Hui Shan",
            "expiry_date": "2026-02-28",
            "renewal_premium": "1150.00",
            "payment_due_date": "2026-02-14",
        },
    },
    {
        "doc_id": "b2-0008",
        "template": "privatecare_policy_wording.html",
        "filename": "b2-0008_Marcus_PrivateCare_FullPolicy.pdf",
        "data": {
            "doc_id": "b2-0008",
            "insurer": "Meridian Assurance",
            "policy_no": "PH-2022-604188",
            "insured": "Marcus Lim Jun Wei",
            "product_name": "PrivateCare Hospital and Surgical Plan",
            "cover_from": "2026-03-01",
            "expiry_date": "2027-02-28",
            "premium_payable": "1860.00",
            "sum_insured": "1,000,000.00",
            "excess": "3,500.00",
        },
    },
    {
        "doc_id": "b2-0009",
        "template": "hospital_income_policy_wording.html",
        "filename": "b2-0009_Dad_HospitalIncome_FullPolicy.pdf",
        "data": {
            "doc_id": "b2-0009",
            "insurer": "Lionhead Life Assurance",
            "policy_no": "HS-2023-771904",
            "insured": "Lim Ah Kow",
            "product_name": "Hospital Income Protection Plan",
            "cover_from": "2026-01-15",
            "expiry_date": "2027-01-14",
            "premium_payable": "2140.00",
        },
    },
    {
        "doc_id": "b2-0010",
        "template": "housing_loan_facility_letter.html",
        "filename": "b2-0010_Housing_Loan_Facility_Letter.pdf",
        "data": {
            "doc_id": "b2-0010",
        },
    },
    {
        "doc_id": "b2-0019",
        "template": "protectplus_life_with_riders.html",
        "filename": "b2-0019_Marcus_LifePolicy_Schedule.pdf",
        "data": {
            "doc_id": "b2-0019",
            "insurer": "Lionhead Life Assurance",
            "policy_no": "LF-2026-641205",
            "insured": "Marcus Lim Jun Wei",
            "product_name": "Lionhead ProtectPlus Life Plan",
            "cover_from": "2026-07-01",
            "expiry_date": "2066-06-30",
            "premium_payable": "2960.00",
            "sum_insured": "200000.00",
        },
    },
    {
        "doc_id": "b2-0011",
        "template": "car_loan_agreement.html",
        "filename": "b2-0011_Car_Loan_Hire_Purchase_Agreement.pdf",
        "data": {
            "doc_id": "b2-0011",
        },
    },
]


def find_browser_executable() -> Path | None:
    """Find Microsoft Edge or Google Chrome executable on Windows."""
    candidates = [
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    ]
    for c in candidates:
        if c.is_file():
            return c
    return None


def generate_documents(output_dir: Path, as_pdf: bool = True) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    temp_dir = output_dir / "_temp_html"
    temp_dir.mkdir(parents=True, exist_ok=True)

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    browser_exe = find_browser_executable() if as_pdf else None

    print(f"Generating {len(DOCUMENTS)} documents to: {output_dir}")
    if as_pdf:
        if browser_exe:
            print(f"Using browser for PDF compilation: {browser_exe}")
        else:
            print("Notice: No headless browser found. Saving rendered HTML files instead.")

    for item in DOCUMENTS:
        template = env.get_template(item["template"])
        html_content = template.render(**item["data"])

        html_file = temp_dir / f"{item['doc_id']}.html"
        html_file.write_text(html_content, encoding="utf-8")

        pdf_name = f"{item['doc_id']}.pdf"
        pdf_file = output_dir / pdf_name

        if as_pdf and browser_exe:
            cmd = [
                str(browser_exe),
                "--headless",
                "--disable-gpu",
                "--no-margins",
                f"--print-to-pdf={pdf_file.resolve()}",
                str(html_file.resolve()),
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"  [OK] Generated PDF: {pdf_file.name}")
            else:
                print(f"  [FAIL] Failed {html_file.name}: {res.stderr}")
        else:
            print(f"  [HTML] Rendered {html_file.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic Lim family documents")
    parser.add_argument(
        "--output", type=Path, default=Path("inbox"), help="Output directory (default: inbox/)"
    )
    parser.add_argument(
        "--html-only", action="store_true", help="Generate HTML without compiling to PDF"
    )
    args = parser.parse_args()

    generate_documents(args.output, as_pdf=not args.html_only)
