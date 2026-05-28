import sys
import os

from scanner.extractor import extract_text_from_pdf
from scanner.detectors import detect_pii
from scanner.scorer import determine_risk
from scanner.reporter import generate_report


def main():

    # Check command line arguments
    if len(sys.argv) < 2:

        print(
            "Usage: python main.py <pdf_file> [--investigation]"
        )

        return

    pdf_path = sys.argv[1]

    # Investigation mode flag
    investigation_mode = False

    if len(sys.argv) == 3:

        if sys.argv[2] == "--investigation":

            investigation_mode = True

            print("[!] Investigation mode enabled.")

    # Check if file exists
    if not os.path.exists(pdf_path):

        print(f"Error: File not found -> {pdf_path}")

        return

    # Extract text
    text = extract_text_from_pdf(pdf_path)

    if not text:

        print("No readable text found in PDF.")

        return

    # Detect PII
    findings = detect_pii(
        text,
        investigation_mode
    )

    # Determine risk
    overall_risk = determine_risk(findings)

    # Generate report
    report = generate_report(
        pdf_path,
        findings,
        overall_risk
    )

    # Print report
    print(report)

    # Create report filename
    base_name = os.path.basename(pdf_path)

    file_name_without_ext = os.path.splitext(
        base_name
    )[0]

    report_path = (
        f"reports/{file_name_without_ext}_report.txt"
    )

    # Save report
    with open(report_path, "w") as f:

        f.write(report)

    print(f"\nReport saved to {report_path}")


if __name__ == "__main__":
    main()