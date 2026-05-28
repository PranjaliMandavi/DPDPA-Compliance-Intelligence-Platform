def determine_risk(findings):
    """
    Determines overall risk level
    from detected findings.
    """

    overall_risk = "LOW"

    for finding in findings:

        severity = finding["risk"]

        if severity == "CRITICAL":
            overall_risk = "CRITICAL"
            break

        elif severity == "HIGH" and overall_risk != "CRITICAL":
            overall_risk = "HIGH"

        elif (
            severity == "MEDIUM"
            and overall_risk not in ["CRITICAL", "HIGH"]
        ):
            overall_risk = "MEDIUM"

    return overall_risk