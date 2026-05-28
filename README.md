# DPDPA Compliance Intelligence Platform

> OCR-powered PII detection and privacy compliance scanner built for India's Digital Personal Data Protection Act (DPDPA 2023).

---

## What It Does

Scans PDF documents — including **scanned/image-based PDFs** — for sensitive personal data, classifies risk levels, and generates forensic compliance reports.

Most PII scanners only work on text-based PDFs. This one uses OCR to handle real-world documents like Aadhaar cards, PAN cards, and scanned forms.

---

## Features

| Feature | Details |
|---|---|
| OCR Pipeline | Handles scanned PDFs, photos, screenshots via Tesseract |
| Aadhaar Detection | Regex-based, with VID disambiguation |
| PAN Detection | Full format validation |
| VID Classification | Contextual — distinguishes Virtual ID from Aadhaar |
| Risk Engine | CRITICAL / HIGH / MEDIUM scoring |
| Masking | All PII masked by default in output |
| Investigation Mode | Unmasked forensic output for authorized review |
| Compliance Reports | Auto-generated `.txt` reports per document |
| Dashboard | Streamlit UI with charts, findings table, download |

---

## Architecture

```
Input PDF
    │
    ├── Text-based ──► pdfplumber ──► raw text
    │
    └── Image-based ──► pdf2image ──► Tesseract OCR ──► raw text
                                              │
                                     PII Detection Engine
                                     (Regex patterns)
                                              │
                                     Risk Classification
                                              │
                                     Masked / Forensic Report
```

---

## Tech Stack

- **Python 3.x**
- **Streamlit** — dashboard UI
- **pdfplumber** — text PDF extraction
- **Tesseract OCR + pytesseract** — image PDF extraction
- **pdf2image + Pillow** — PDF to image conversion
- **Plotly** — risk distribution charts
- **pandas** — findings table

---

## Project Structure

```
dpdpa-scanner/
│
├── scanner/
│   ├── extractor.py       # OCR + text extraction logic
│   ├── detectors.py       # PII regex patterns + masking
│   ├── scorer.py          # Risk classification
│   └── reporter.py        # Report generation
│
├── samples/               # Test documents
├── reports/               # Generated reports (gitignored)
├── assets/                # Screenshots
│
├── app.py                 # Streamlit dashboard
├── main.py                # CLI entry point
├── requirements.txt
└── README.md
```

---

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/dpdpa-compliance-platform.git
cd dpdpa-compliance-platform

pip install -r requirements.txt
```

### Tesseract (required for OCR)

- **Windows:** Download installer from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
- **Linux:** `sudo apt install tesseract-ocr`
- **Mac:** `brew install tesseract`

Then set the path in `scanner/extractor.py`:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\path\to\tesseract.exe"
```

---

## Usage

### CLI

```bash
# Scan a single PDF
python main.py samples/Adharcard.pdf

# Investigation mode (shows unmasked values)
python main.py samples/Adharcard.pdf --investigation
```

### Dashboard

```bash
streamlit run app.py
```

Upload a PDF → click **Start Security Scan** → view findings, chart, and download report.

---

## Sample Output

```
==================================================
DPDPA COMPLIANCE REPORT
==================================================

Scanned File: Adharcard.pdf

Detected PII:
--------------------------------------------------

[CRITICAL] Aadhaar Number
Detected Value : 4559 XXXX XXXX

[HIGH] Virtual ID (VID)
Detected Value : VID: 9181 XXXX XXXX

[MEDIUM] Email Address
Detected Value : el***@uidal.gov.in

[MEDIUM] Date of Birth
Detected Value : 09/08/2003

--------------------------------------------------
Overall Risk Level: CRITICAL
```

---

## Engineering Challenges Solved

**1. VID vs Aadhaar overlap** — Both are 12-digit numbers. Solved by checking for `VID:` prefix contextually before applying the Aadhaar pattern.

**2. OCR on real documents** — Aadhaar cards and scanned forms are image-based. Integrated Tesseract pipeline as a fallback when pdfplumber returns no text.

**3. Duplicate suppression** — Same number appearing multiple times in a document is deduplicated in the final report.

**4. Forensic vs compliance mode** — Two output modes: masked (safe to share) and unmasked (investigation only).

---

## Limitations

- OCR accuracy depends on image quality and scan resolution
- Currently supports PDF format only
- Regex patterns may produce false positives on unusual formatting
- Designed for Indian documents (Aadhaar, PAN, VID)

---

## Roadmap

- [ ] JSON report export for SIEM integration
- [ ] Folder/batch scanning
- [ ] Confidence scoring per detection
- [ ] Support for image files (JPG, PNG) directly
- [ ] Cloud deployment (Streamlit Cloud)

---

## Compliance Context

Built in the context of **DPDPA 2023** (India's data protection law), which requires organizations to identify, protect, and minimize exposure of personal data. This tool helps detect potential violations before documents are shared or published.

---

## Author

Built as part of a cybersecurity + privacy compliance portfolio project.
