def generate_report(file_name, findings, overall_risk):
    """
    Generates formatted compliance report.
    """

    report = []

    report.append("=" * 50)
    report.append("DPDPA COMPLIANCE REPORT")
    report.append("=" * 50)

    report.append(f"\nScanned File: {file_name}")

    report.append("\nDetected PII:")
    report.append("-" * 50)

    if not findings:
        report.append("No sensitive information detected.")

    else:

        for finding in findings:

            report.append(
                f"\n[{finding['risk']}] {finding['type']}"
            )

            report.append(
                f"Detected Value : {finding['masked_value']}"
            )

    report.append("\n" + "-" * 50)
    report.append(f"Overall Risk Level: {overall_risk}")

    report.append("\nRecommendations:")

    if overall_risk == "CRITICAL":

        report.append(
            "- Immediately redact government-issued identifiers."
        )

        report.append(
            "- Restrict public document exposure."
        )

    elif overall_risk == "HIGH":

        report.append(
            "- Review personal data sharing policies."
        )

        report.append(
            "- Apply masking for sensitive fields."
        )

    elif overall_risk == "MEDIUM":

        report.append(
            "- Minimize unnecessary personal data exposure."
        )

    else:

        report.append(
            "- Maintain current privacy safeguards."
        )

    return "\n".join(report)