import re

# ─────────────────────────────────────────
# PII PATTERNS CONFIGURATION
# ─────────────────────────────────────────

PATTERNS = {

    "aadhaar": {
        "regex": r"\b[2-9][0-9]{3}\s[0-9]{4}\s[0-9]{4}\b",
        "risk": "CRITICAL",
        "description": "Aadhaar Number"
    },

    "vid": {
        "regex": r"(?i)(?:VID|Virtual ID)[^\d]{0,10}(?:[0-9]{4}\s[0-9]{4}\s[0-9]{4})",
        "risk": "HIGH",
        "description": "Virtual ID (VID)"
    },

    "pan": {
        "regex": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
        "risk": "CRITICAL",
        "description": "PAN Card Number"
    },

    "phone": {
        "regex": r"\b(?:\+91[\-\s]?)?[6-9]\d{9}\b",
        "risk": "HIGH",
        "description": "Indian Phone Number"
    },

    "email": {
        "regex": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "risk": "MEDIUM",
        "description": "Email Address"
    },

    "dob": {
        "regex": (
            r"\b(?:"

            # DD-MM-YYYY or DD/MM/YYYY
            r"(?:0[1-9]|[12][0-9]|3[01])[-/](?:0[1-9]|1[0-2])[-/](?:19|20)\d{2}"

            r"|"

            # MM-DD-YYYY or MM/DD/YYYY
            r"(?:0[1-9]|1[0-2])[-/](?:0[1-9]|[12][0-9]|3[01])[-/](?:19|20)\d{2}"

            r"|"

            # YYYY-DD-MM or YYYY/DD/MM
            r"(?:19|20)\d{2}[-/](?:0[1-9]|[12][0-9]|3[01])[-/](?:0[1-9]|1[0-2])"

            r"|"

            # YYYY-MM-DD or YYYY/MM/DD
            r"(?:19|20)\d{2}[-/](?:0[1-9]|1[0-2])[-/](?:0[1-9]|[12][0-9]|3[01])"

            r")\b"
        ),
        "risk": "MEDIUM",
        "description": "Date of Birth"
    }
}


# ─────────────────────────────────────────
# MASKING FUNCTION
# ─────────────────────────────────────────

def mask_value(value, investigation_mode=False):
    """
    Masks sensitive information before reporting.
    """

    # Show full values in investigation mode
    if investigation_mode:
        return value

    # Email masking
    if "@" in value:

        username, domain = value.split("@")

        return username[:2] + "***@" + domain

    # Aadhaar masking
    if re.fullmatch(r"[2-9][0-9]{3}\s[0-9]{4}\s[0-9]{4}", value):

        return value[:4] + " XXXX XXXX"

    # VID masking
    if "VID" in value.upper() or "VIRTUAL ID" in value.upper():

        digits = re.findall(r"\d{4}", value)

        if len(digits) == 3:

            return f"VID: {digits[0]} XXXX XXXX"

    # PAN masking
    if re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", value):

        return value[:2] + "*****" + value[-2:]

    # Phone masking
    if re.fullmatch(r"(?:\+91[\-\s]?)?[6-9]\d{9}", value):

        return value[:4] + "******"

    return value


# ─────────────────────────────────────────
# MAIN DETECTION FUNCTION
# ─────────────────────────────────────────

def detect_pii(text, investigation_mode=False):
    """
    Detects PII from extracted text.
    Returns structured findings list.
    """

    findings = []

    # Store exact VID numbers
    detected_vid_values = set()

    # ─────────────────────────────────────
    # FIRST PASS → DETECT VID
    # ─────────────────────────────────────

    vid_config = PATTERNS["vid"]

    vid_matches = re.finditer(vid_config["regex"], text)

    for match in vid_matches:

        original_value = match.group()

        digits = re.findall(r"\d{4}", original_value)

        if len(digits) == 3:

            cleaned_vid = " ".join(digits)

            detected_vid_values.add(cleaned_vid)

            findings.append({
                "type": vid_config["description"],
                "value": original_value,
                "masked_value": mask_value(
                    original_value,
                    investigation_mode
                ),
                "risk": vid_config["risk"]
            })

    # ─────────────────────────────────────
    # SECOND PASS → DETECT OTHER PII
    # ─────────────────────────────────────

    for pii_type, config in PATTERNS.items():

        # Skip VID because already processed
        if pii_type == "vid":
            continue

        matches = re.finditer(config["regex"], text)

        for match in matches:

            original_value = match.group()

            # Prevent VID from becoming Aadhaar
            if pii_type == "aadhaar":

                if original_value in detected_vid_values:
                    continue

            findings.append({
                "type": config["description"],
                "value": original_value,
                "masked_value": mask_value(
                    original_value,
                    investigation_mode
                ),
                "risk": config["risk"]
            })

    # ─────────────────────────────────────
    # REMOVE DUPLICATES
    # ─────────────────────────────────────

    unique_findings = []

    seen = set()

    for finding in findings:

        key = (
            finding["type"],
            finding["masked_value"]
        )

        if key not in seen:

            seen.add(key)

            unique_findings.append(finding)

    return unique_findings