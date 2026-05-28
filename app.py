import streamlit as st
import pandas as pd
import tempfile
import os

from scanner.extractor import extract_text_from_pdf
from scanner.detectors import detect_pii
from scanner.scorer import determine_risk
from scanner.reporter import generate_report


# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────

st.set_page_config(
    page_title="DPDPA Cyber Dashboard",
    page_icon="🛡️",
    layout="wide"
)


# ─────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────

st.markdown("""
<style>

body {
    background-color: #0f1117;
}

.main {
    background-color: #0f1117;
    color: white;
}

.block-container {
    padding-top: 2rem;
}

.metric-card {
    background-color: #161b22;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #30363d;
    text-align: center;
}

.metric-title {
    font-size: 18px;
    color: #8b949e;
}

.metric-value {
    font-size: 28px;
    font-weight: bold;
}

.critical {
    color: #ff4b4b;
}

.high {
    color: #ff9800;
}

.medium {
    color: #ffd700;
}

.low {
    color: #00c853;
}

.section-card {
    background-color: #161b22;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #30363d;
    margin-top: 20px;
}

.sidebar .sidebar-content {
    background-color: #0d1117;
}

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────

st.sidebar.title("🛡️ DPDPA Scanner")

st.sidebar.markdown("---")

investigation_mode = st.sidebar.toggle(
    "Investigation Mode"
)

st.sidebar.markdown("""
### Features
- OCR Support
- Aadhaar Detection
- PAN Detection
- VID Classification
- Investigation Mode
- Risk Classification
""")


# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────

st.title("🛡️ DPDPA Compliance Dashboard")

st.markdown("""
Cybersecurity & Privacy Compliance Analysis Console
""")


# ─────────────────────────────────────────
# FILE UPLOAD
# ─────────────────────────────────────────

uploaded_file = st.file_uploader(
    "Upload PDF Document",
    type=["pdf"]
)


# ─────────────────────────────────────────
# MAIN SCAN LOGIC
# ─────────────────────────────────────────

if uploaded_file:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp_file:

        tmp_file.write(uploaded_file.read())

        temp_pdf_path = tmp_file.name

    st.success("PDF uploaded successfully.")

    if st.button("🔍 Scan Document"):

        with st.spinner("Analyzing document..."):

            # Extract text
            text = extract_text_from_pdf(temp_pdf_path)

            # Detect PII
            findings = detect_pii(
                text,
                investigation_mode
            )

            # Determine risk
            overall_risk = determine_risk(findings)

            # Generate report
            report = generate_report(
                uploaded_file.name,
                findings,
                overall_risk
            )

        # ─────────────────────────────────
        # METRICS
        # ─────────────────────────────────

        critical_count = sum(
            1 for f in findings
            if f["risk"] == "CRITICAL"
        )

        high_count = sum(
            1 for f in findings
            if f["risk"] == "HIGH"
        )

        medium_count = sum(
            1 for f in findings
            if f["risk"] == "MEDIUM"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">
                    Overall Risk
                </div>
                <div class="metric-value critical">
                    {overall_risk}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">
                    Critical Findings
                </div>
                <div class="metric-value critical">
                    {critical_count}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">
                    High Findings
                </div>
                <div class="metric-value high">
                    {high_count}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">
                    Medium Findings
                </div>
                <div class="metric-value medium">
                    {medium_count}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ─────────────────────────────────
        # FINDINGS TABLE
        # ─────────────────────────────────

        st.markdown("## 📋 Detected PII")

        findings_df = pd.DataFrame(findings)

        if not findings_df.empty:

            findings_df = findings_df[
                ["type", "risk", "masked_value"]
            ]

            findings_df.columns = [
                "PII Type",
                "Risk Level",
                "Detected Value"
            ]

            st.dataframe(
                findings_df,
                use_container_width=True
            )

        else:
            st.info("No PII detected.")

        # ─────────────────────────────────
        # REPORT SECTION
        # ─────────────────────────────────

        st.markdown("## 📄 Compliance Report")

        st.text_area(
            "Generated Report",
            report,
            height=300
        )

        # ─────────────────────────────────
        # DOWNLOAD REPORT
        # ─────────────────────────────────

        st.download_button(
            label="⬇ Download Report",
            data=report,
            file_name="compliance_report.txt",
            mime="text/plain"
        )

    # Cleanup temp file
    os.unlink(temp_pdf_path)