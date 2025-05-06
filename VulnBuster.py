import streamlit as st
import re

# App Configuration
st.set_page_config(
    page_title="Secure Code Review Tool",
    page_icon="🛡️",
    layout="centered"
)

# --- Header ---
st.title("🛡️ Secure Code Review Tool")
st.markdown(
    "Analyze your code for **common security vulnerabilities**. "
    "Paste your code below and click 'Scan' to get started."
)

# --- Code Input ---
st.subheader("📥 Paste Your Code")
code_input = st.text_area("Enter your Python code here:", height=300)

# --- Scan Logic ---
def basic_security_scan(code):
    issues = []

    # Rule-based pattern checks
    if "eval(" in code:
        issues.append("⚠️ `eval()` is dangerous and can lead to code injection.")
    if "exec(" in code:
        issues.append("⚠️ `exec()` allows arbitrary code execution. Avoid using it.")
    if "pickle.load" in code:
        issues.append("⚠️ `pickle.load` can execute arbitrary code if the source is untrusted.")
    if re.search(r'password\s*=\s*["\'].*["\']', code, re.IGNORECASE):
        issues.append("⚠️ Hardcoded password detected. Use environment variables instead.")
    if "os.system(" in code:
        issues.append("⚠️ `os.system` can be risky. Use `subprocess.run()` for better security.")
    if "input(" in code:
        issues.append("⚠️ Validate user input to prevent unexpected behavior or injection.")

    if not issues:
        return ["✅ No obvious vulnerabilities found. Your code looks good!"]
    return issues

# --- Scan Button ---
if st.button("🔍 Scan for Vulnerabilities"):
    if not code_input.strip():
        st.warning("Please paste some code to scan.")
    else:
        st.subheader("🧪 Scan Results")
        results = basic_security_scan(code_input)
        for result in results:
            st.write(result)

# --- Footer ---
st.markdown("---")
st.caption("© 2025 VulnBuster | Built with ❤️ using Streamlit")


