import pdfplumber
import pytesseract

from pdf2image import convert_from_path


# ─────────────────────────────────────────
# TESSERACT OCR PATH
# ─────────────────────────────────────────

pytesseract.pytesseract.tesseract_cmd = (
    r"E:\2026\project2\ocr\tesseract.exe"
)


# ─────────────────────────────────────────
# TEXT-BASED PDF EXTRACTION
# ─────────────────────────────────────────

def extract_text_using_pdfplumber(pdf_path):
    """
    Extracts text using pdfplumber.
    Works best for digital/text PDFs.
    """

    full_text = ""

    try:

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    full_text += page_text + "\n"

    except Exception as e:

        print(f"[ERROR] PDF extraction failed: {e}")

    return full_text


# ─────────────────────────────────────────
# OCR EXTRACTION
# ─────────────────────────────────────────

def extract_text_using_ocr(pdf_path):
    """
    Uses OCR for scanned/image PDFs.
    """

    full_text = ""

    try:

        images = convert_from_path(
            pdf_path,
            poppler_path=(
                r"E:\2026\project2\Release-26.02.0-0"
                r"\poppler-26.02.0\Library\bin"
            )
        )

        for page_number, image in enumerate(images, start=1):

            print(f"[*] Running OCR on page {page_number}...")

            text = pytesseract.image_to_string(image)

            full_text += text + "\n"

    except Exception as e:

        print(f"[ERROR] OCR extraction failed: {e}")

    return full_text


# ─────────────────────────────────────────
# MAIN EXTRACTION FUNCTION
# ─────────────────────────────────────────

def extract_text_from_pdf(pdf_path):
    """
    Main extraction pipeline.

    1. Try text extraction first
    2. If empty -> fallback to OCR
    """

    print("\n[*] Attempting normal PDF text extraction...")

    text = extract_text_using_pdfplumber(pdf_path)

    # If text found → use it
    if text.strip():

        print("[+] Text-based PDF detected.")

        return text

    # Otherwise → OCR fallback
    print("[!] No readable text found.")
    print("[*] Falling back to OCR extraction...")

    ocr_text = extract_text_using_ocr(pdf_path)

    if ocr_text.strip():

        print("[+] OCR extraction successful.")

        return ocr_text

    print("[!] OCR extraction failed.")

    return ""