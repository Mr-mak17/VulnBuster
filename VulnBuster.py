import streamlit as st
import re

st.set_page_config(page_title="Secure Code Review", layout="centered")

st.title("🛡️ Secure Code Review Tool")
st.write("Paste your code below and scan for basic security risks.")

code_input = st.text_area("Your Code:", height=300)

def basic_security_scan(code):
    issues = []

    if "eval(" in code:
        issues.append("⚠️ Avoid using `eval()` — it's a major security risk.")
    if "exec(" in code:
        issues.append("⚠️ Avoid `exec()` — it can run arbitrary code.")
    if re.search(r'password\s*=\s*["\'].*["\']', code):
        issues.append("⚠️ Hardcoded passwords found — use environment variables.")
    if "import os" in code and "os.system" in code:
        issues.append("⚠️ Use of `os.system` — prefer safer subprocess methods.")
    
    if not issues:
        return ["✅ No obvious issues found."]
    return issues

if st.button("🔍 Scan for Vulnerabilities"):
    results = basic_security_scan(code_input)
    for r in results:
        st.write(r)
