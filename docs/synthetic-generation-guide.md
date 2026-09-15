# Project Parrot: Synthetic Document & Specimen Generation Guide

This guide provides the **amended Gemini image generation prompt bank** (fictionalised for the **Republic of Xinkapow**) and the **Jupyter notebook workflow** to generate complete, multi-page synthetic documents for the Lim household.

All parameters adhere strictly to [`corpus/canon.md`](../corpus/canon.md) and carry the required synthetic watermarks.

---

## 1. Ground Truth Parameters (Canonical Lim Household & Xinkapow)

To ensure strict legal compliance and eliminate resemblance to official Singapore National Registration Identity Cards:
- **Country / Jurisdiction:** **Republic of Xinkapow**
- **ID Card Color Scheme:** Dominant **Yellow and Orange** guilloche security patterns
- **Emblem / Crest:** **KFC Mascot** (distinguished smiling bearded elder with black string tie) replacing national coats of arms / Merlions.
- **Mandatory Watermark:** `PROJECT PARROT · SYNTHETIC SPECIMEN · FOR RESEARCH EVALUATION ONLY`

| Subject | Role | ID Number (Mod-11 Valid) | DOB | Employer / Status | Notes |
|---|---|---|---|---|---|
| **Marcus Lim Jun Wei** | Owner (`self`) | `S8714289B` | 1987-05-08 | Meridian Systems Pte Ltd | IT Manager; $9,400.00/mo |
| **Rachel Ng Hui Shan** | Wife (`partner`) | `S8923156F` | 1989-02-17 | Northlight Health Pte Ltd | Senior Physiotherapist; $6,250.00/mo |
| **Lucas Lim Kai En** | Son (`child`) | `T1942088J` | 2019-06-14 | Primary 1 Student | Born at KK Women's and Children's Hospital |
| **Lim Ah Kow** | Father (`parent`) | `S5809142A` | 1958-10-12 | Retiree | Hypertension & diabetes; resident from 2021 |
| **Tan Mei Ling** | Mother (`parent`) | `S6134891C` | 1961-04-25 | Retiree / Homemaker | Osteoporosis; resident from 2021 |

- **Canonical Address:** `Blk 45B Tampines Ave 8, #07-21, Xinkapow 521045` (effective from 2021-03-06).
- **Approved Insurers:** `Meridian Assurance`, `Lionhead Life Assurance`.
- **Financing Bank:** `Crescent Bank Limited` (Housing Mortgage & Auto Finance).

---

## 2. Amended Gemini Prompts Bank (Xinkapow Yellow/Orange Cards with KFC Mascot)

Use these prompts directly in Gemini to generate photorealistic image files (`.png` / `.jpg`). Once generated, save them into [`inbox/`](../inbox/) for Parrot ingestion testing.

### 2.1 Marcus Lim Jun Wei — Xinkapow National Identity Card (Front)
```text
Photorealistic high-resolution scan of the front side of a modern national identity card issued by the fictional REPUBLIC OF XINKAPOW, flat lay on a clean wooden desk.
Card Aesthetics:
- Color Palette: Vibrant two-tone Warm Yellow (#FFC72C) and Sunset Orange (#FF8200) with intricate geometric guilloche micro-printing.
- Top Header: Bold dark navy typography reading 'REPUBLIC OF XINKAPOW' and 'NATIONAL IDENTITY CARD'.
- Official Mascot Emblem: At top center/right, an official circular gold security seal depicting a stylized KFC Mascot (a distinguished smiling silver-bearded elder wearing black-rimmed glasses and a neat black ribbon string tie).
Card Data Particulars:
- Identity Number: S8714289B
- Full Name: MARCUS LIM JUN WEI
- Race: CHINESE
- Date of Birth: 08-05-1987
- Sex: M
- Country of Birth: XINKAPOW
Portrait Photo: Professional Chinese male in his late 30s, neat short black hair, collared dark business shirt, clean shaven, friendly neutral expression.
Secondary Ghost Image: Small translucent grayscale duplicate of the portrait in the lower right corner.
Watermark across card: Distinct semi-transparent diagonal crimson red stamp (-30 degrees angle) reading: 'PROJECT PARROT · SYNTHETIC SPECIMEN · FOR RESEARCH EVALUATION ONLY'.
Pristine optical clarity, sharp micro-text, realistic laminated card finish with rounded edges.
```

### 2.2 Marcus Lim Jun Wei — Xinkapow National Identity Card (Back)
```text
Photorealistic high-resolution scan of the back side of a national identity card from the REPUBLIC OF XINKAPOW.
Card Aesthetics:
- Background security pattern in subtle light orange and pale yellow wave patterns.
- Card Particulars:
  - Address: BLK 45B TAMPINES AVE 8 #07-21 XINKAPOW 521045
  - Date of Issue: 15-06-2017
  - Postcode: 521045
- Technical Features: Standard black magnetic stripe at the top, high-density 2D barcode strip at the bottom, and a biometric thumbprint sensor box.
Watermark: A distinct semi-transparent diagonal crimson red stamp reading: 'PROJECT PARROT · SYNTHETIC SPECIMEN · FOR RESEARCH EVALUATION ONLY'.
Sharp focus, authentic plastic card texture, perfectly legible typography.
```

---

### 2.3 Rachel Ng Hui Shan — Xinkapow National Identity Card (Front)
```text
Photorealistic high-resolution scan of the front side of a modern national identity card for the REPUBLIC OF XINKAPOW, flat lay.
Card Aesthetics:
- Color Palette: Warm Yellow and Citrus Orange guilloche security line patterns with fine micro-printing.
- Header: 'REPUBLIC OF XINKAPOW' & 'NATIONAL IDENTITY CARD'.
- Mascot: A polished gold-foil crest in the top corner depicting the KFC Mascot (smiling elder with white beard, spectacles, and string bow tie).
Card Data:
- Identity Number: S8923156F
- Full Name: RACHEL NG HUI SHAN
- Race: CHINESE
- Date of Birth: 17-02-1989
- Sex: F
- Country of Birth: XINKAPOW
Portrait Photo: Professional Chinese female in her mid 30s, shoulder-length neat black hair, pleasant professional expression, wearing a navy collared blouse.
Secondary Ghost Image: Miniature grayscale portrait in lower right.
Watermark: Prominent diagonal semi-transparent red watermark reading: 'PROJECT PARROT · SYNTHETIC SPECIMEN · FOR RESEARCH EVALUATION ONLY'.
Ultra-sharp micro-typography, realistic card laminate.
```

### 2.4 Rachel Ng Hui Shan — Xinkapow National Identity Card (Back)
```text
Photorealistic scan of the reverse side of an official identity card from the REPUBLIC OF XINKAPOW.
Background in pale orange security micro-printing.
Card Details:
- Address: BLK 45B TAMPINES AVE 8 #07-21 XINKAPOW 521045
- Date of Issue: 20-03-2019
- Postcode: 521045
Machine-readable code strip along lower margin, card serial number at top.
Watermark: Semi-transparent diagonal red stamp: 'PROJECT PARROT · SYNTHETIC SPECIMEN · FOR RESEARCH EVALUATION ONLY'.
High resolution, rounded plastic corners.
```

---

### 2.5 Lim Ah Kow (Father) — Xinkapow Senior Citizen Identity Card
```text
Photorealistic scan of a senior citizen national identity card from the REPUBLIC OF XINKAPOW.
Card Aesthetics:
- Rich Golden Yellow and Amber Orange dual-toned guilloche background.
- Official KFC Mascot gold seal prominently displayed at the top.
Card Details:
- Identity Number: S5809142E
- Full Name: LIM AH KOW
- Race: CHINESE
- Date of Birth: 12-10-1958
- Sex: M
- Country of Birth: XINKAPOW
Portrait Photo: Chinese senior gentleman in his late 60s, silver-grey hair, dignified warm smile, wearing a casual polo shirt.
Watermark: 'PROJECT PARROT · SYNTHETIC SPECIMEN · FOR RESEARCH EVALUATION ONLY' in semi-transparent red across card face.
Macro texture, authentic identity document styling.
```

---

### 2.6 Tan Mei Ling (Mother) — Xinkapow Senior Citizen Identity Card
```text
Photorealistic scan of a senior citizen national identity card from the REPUBLIC OF XINKAPOW.
Card Aesthetics:
- Elegant Yellow-and-Orange radial security linework with official KFC Mascot crest in upper header.
Card Details:
- Identity Number: S6134891C
- Full Name: TAN MEI LING
- Race: CHINESE
- Date of Birth: 25-04-1961
- Sex: F
- Country of Birth: XINKAPOW
Portrait Photo: Chinese senior lady in her mid 60s, short perm hair, wearing reading glasses, gentle smiling demeanor.
Watermark: 'PROJECT PARROT · SYNTHETIC SPECIMEN · FOR RESEARCH EVALUATION ONLY' in diagonal semi-transparent red banner.
Sharp focus, crisp security lines.
```

---

### 2.7 Lucas Lim Kai En — Xinkapow Digital Birth Certificate
```text
High-resolution official document scan of an official Digital Birth Certificate issued by the Immigration and Civil Registration Authority of the REPUBLIC OF XINKAPOW.
Design & Typography:
- Official document header featuring the national crest of Xinkapow (embossed gold KFC Mascot crest with laurel leaves).
- Formal government certificate borders with subtle yellow-orange guilloche background.
Certificate Particulars:
- Birth Registration Number: T1942088J
- Child's Full Name: LUCAS LIM KAI EN
- Sex: MALE
- Date & Time of Birth: 14 JUNE 2019, 09:42 HRS
- Place of Birth: KK WOMEN'S AND CHILDREN'S HOSPITAL, XINKAPOW
- Father's Name: MARCUS LIM JUN WEI (ID: S8714289B)
- Mother's Name: RACHEL NG HUI SHAN (ID: S8923156F)
- Informant: MARCUS LIM JUN WEI (FATHER)
Watermark: Prominent diagonal translucent banner reading: 'PROJECT PARROT · SYNTHETIC TEST RECORD · NOT A REAL DOCUMENT'.
Clean A4 official layout with verification QR badge in bottom right.
```

---

## 3. Comprehensive Document Suite: Policy Wordings & Loan Agreements

All multi-page contracts are generated via [`notebooks/generate_lim_documents.py`](../notebooks/generate_lim_documents.py) or [`notebooks/generate_lim_documents.ipynb`](../notebooks/generate_lim_documents.ipynb).

### 3.1 Marcus's PrivateCare Hospital & Surgical Plan (`b2-0008.pdf`)
* **Template:** [`corpus/templates/privatecare_policy_wording.html`](../corpus/templates/privatecare_policy_wording.html) (4 pages)
* **Clinical Provisions Included:**
  * **Heart Stent Coverage:** Clause 4.1 & Table 5 explicitly cover *Percutaneous Transluminal Coronary Angioplasty (PTCA) with Stent Insertion (Drug-Eluting / Bare-Metal Stents)* as **COVERED AS CHARGED** up to the SGD $1,000,000.00 annual limit (subject to $3,500 deductible and 10% co-insurance).
  * **Kidney Stones:** Clause 4.2 covers inpatient stone surgeries (PCNL/URS laser lithotripsy) as-charged; day-surgery ESWL covered up to 5 sessions per policy year.
  * **15 Explicit Policy Exclusions:** Pre-existing conditions, experimental treatments (not HSA-approved), cosmetic surgery, routine check-ups, non-accidental dental, self-inflicted injuries, pregnancy/fertility, congenital anomalies, psychiatric conditions, alternative medicine (TCM), refractive errors, STDs/HIV, war/military, rest cures, supplements.

### 3.2 Dad's Hospital Income Protection Plan (`b2-0009.pdf`)
* **Template:** [`corpus/templates/hospital_income_policy_wording.html`](../corpus/templates/hospital_income_policy_wording.html) (3 pages)
* **Clinical Provisions Included:**
  * **Daily Cash Benefit:** SGD $250.00 / day for qualifying inpatient admissions (minimum 24 consecutive hours).
  * **Kidney Stones Coverage:** Clause 3.2 explicitly states:
    * **YES, covered for inpatient admission:** Hospitalisation for renal calculi (kidney stones) or acute renal colic pays SGD $250.00 per day if admitted as a bed-patient for 24+ consecutive hours.
    * **NO, outpatient ESWL is excluded:** Section 4.3 specifically excludes day-surgery shock wave lithotripsy (ESWL) without overnight hospital admission.

### 3.3 Crescent Bank Residential Housing Loan Facility Letter (`b2-0010.pdf`)
* **Template:** [`corpus/templates/housing_loan_facility_letter.html`](../corpus/templates/housing_loan_facility_letter.html) (3 pages)
* **Loan Terms:** SGD $540,000.00 term loan over 30 years at 3M XORA + 0.65% (2.85% p.a.). Property: Blk 45B Tampines Ave 8 #07-21.
* **Lock-in & Selling Penalties (Clause 7):**
  * **Commitment (Lock-In) Period:** **36 Months (3 Years)**.
  * **Penalty if selling within 6 months:**
    1. **1.50% Prepayment Penalty:** 1.50% of the redeemed loan balance (SGD 8,025.00 on a $535k balance).
    2. **Clawback of Subsidies:** Immediate repayment of bank cash subsidies: **SGD 2,500.00** legal fee + **SGD 500.00** valuation fee = **SGD 3,000.00**.
    3. **Notice Period:** Minimum 3 months' prior written notice required (or 3 months' interest in lieu).
    4. **Total penalty on sale within 6 months:** **SGD 11,525.00** (plus notice interest).

### 3.4 Crescent Bank Motor Vehicle Hire Purchase Agreement (`b2-0011.pdf`)
* **Template:** [`corpus/templates/car_loan_agreement.html`](../corpus/templates/car_loan_agreement.html) (2 pages)
* **Vehicle & Loan:** Marcus Lim's Seven-Seat MPV 1.8 (`SLK 8842 D`). Loan Amount: SGD $65,000.00 over 84 months (7 years) at 2.78% flat p.a.
* **Early Settlement Penalties (Clause 7):**
  * **Penalty if selling within 6 months:**
    1. **Rule of 78 Interest Rebate Penalty:** Bank retains an **administrative penalty deduction of 20%** of the statutory unearned interest rebate.
    2. **Early Termination Penalty Fee:** **1.00% of outstanding loan balance or SGD 500.00 (whichever is higher)** if settled within 12 months.
    3. **Discharge Processing Fee:** Flat **SGD 150.00**.

---

## 4. How to Generate and Drop into `inbox/`

To generate all 11 documents directly into [`inbox/`](../inbox/):

```powershell
python notebooks/generate_lim_documents.py --output inbox
```

---

## 5. Ground Truth Q&A Test Matrix for Parrot

Once the documents are in [`inbox/`](../inbox/), run `scripts/ask.py` to test Parrot's extraction and RAG reasoning:

| Question to Ask Parrot | Ground Truth Answer & Citation |
|---|---|
| **"Tell me my insurance exclusions"** | Lists the 15 exclusions from `b2-0008.pdf` (Page 4, Section 6), citing pre-existing conditions, cosmetic surgery, non-accidental dental, routine check-ups, and alternative medicine (TCM). |
| **"Does my dad's policy cover kidney stones?"** | Explains that under `HS-2023-771904` (`b2-0009.pdf`, Clause 3.2), inpatient hospitalisation for kidney stones is covered at **SGD 250.00/day** (minimum 24h admission), but outpatient ESWL day-surgery is **excluded**. |
| **"Can I go for heart stent operation and is it covered under my policies?"** | Explains that under Marcus's PrivateCare plan (`PH-2022-604188`, `b2-0008.pdf`, Clause 4.1 & Table 5), coronary angioplasty with stent insertion is **covered as charged** (subject to $3,500 deductible and 10% co-insurance). |
| **"If I sell the house within 6 months, do I need to pay any penalty?"** | Explains from `b2-0010.pdf` (Clause 7) that selling within the 36-month lock-in incurs a **1.50% prepayment penalty** on the outstanding loan, plus **SGD 3,000.00 clawback** of legal/valuation subsidies, and requires 3 months' notice. |
| **"If I sell the car within 6 months, do I need to pay any penalty?"** | Explains from `b2-0011.pdf` (Clause 7) that early settlement incurs a **20% deduction penalty on the Rule of 78 interest rebate**, an early termination fee of **1.00% or SGD 500.00**, and an administrative discharge fee of SGD 150.00. |
| **"What is my term life premium?"** | Cites Marcus's whole life policy (`LF-2015-330277`, $3,600/yr), correctly disambiguating Marcus from Rachel's term policy (`LF-2024-883192`, $1,420/yr) per ADR 0011. |
| **"What is Rachel's term life premium?"** | Cites Rachel's LifeGuard Term Plan (`LF-2024-883192`, `b2-0003.pdf`), answering **SGD 1,420.00/year**. |
