import openai
import streamlit as st
import time

# Set your OpenAI API Key (ensure it's set in your environment or replace directly)
openai.api_key = "YOUR_OPENAI_API_KEY"  # Ensure you use your OpenAI API key here

# --- Login Functionality ---
def login(username, password):
    """Basic user login system (you can replace this with a database or API later)"""
    users = {
        "user1": "password1",  # Example user, replace with actual data
        "user2": "password2",
    }
    if username in users and users[username] == password:
        return True
    return False

# --- App Configuration ---
st.set_page_config(
    page_title="AI-Powered Secure Code Review Tool",
    page_icon="🛡️",
    layout="centered"
)

# --- Session State to Manage Login & User Limit ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'usage_count' not in st.session_state:
    st.session_state.usage_count = 0

# --- Header ---
st.title("🛡️ AI-Powered Secure Code Review Tool")
st.markdown(
    "Upload your Python code file below and get AI-powered security analysis for vulnerabilities, best practices, and suggestions for improvement."
)

# --- Login Section ---
if not st.session_state.logged_in:
    st.subheader("👤 Login to Start")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.session_state.usage_count = 0  # Reset usage count on successful login
            st.success("Login Successful!")
        else:
            st.error("Invalid username or password.")
else:
    st.write(f"Welcome back, {username}!")

# --- File Upload Section ---
if st.session_state.logged_in:
    st.subheader("📥 Upload Your Python Code File")
    uploaded_file = st.file_uploader("Choose a .py file", type=["py"])

    # --- AI-based Security Analysis Function ---
    def ai_security_scan(code):
        """Function to get AI-powered security analysis using OpenAI's GPT-3.5"""
        prompt = f"""
        Review the following Python code for potential security vulnerabilities, coding best practices, or any issues. 
        Provide a clear, detailed analysis with suggestions for improvement:

        {code}
        """
        
        try:
            # Making an API call to OpenAI's GPT-3.5 model
            response = openai.Completion.create(
                engine="text-davinci-003",  # Or use the free GPT-3.5 model
                prompt=prompt,
                max_tokens=500,
                temperature=0.3
            )
            # Extracting the AI response
            analysis = response.choices[0].text.strip()
            return analysis
        except Exception as e:
            return f"⚠️ Error in processing your code: {e}"

    # --- Limit User Usage ---
    if uploaded_file is not None:
        if st.session_state.usage_count < 3:
            code_input = uploaded_file.read().decode("utf-8")
            
            # When the user clicks the analyze button
            if st.button("🔍 Analyze Code"):
                if not code_input.strip():
                    st.warning("Please upload a valid Python file.")
                else:
                    st.subheader("🧪 AI Scan Results")
                    # AI-based analysis of the uploaded code
                    results = ai_security_scan(code_input)
                    st.write(results)
                    
                    # Increment usage count
                    st.session_state.usage_count += 1
        else:
            st.error("You have exceeded the maximum number of analyses for this session (3). Please log out and log back in.")
    else:
        st.warning("Please upload a Python code file to analyze.")

# --- Logout Button ---
if st.session_state.logged_in:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.usage_count = 0  # Reset usage count on logout
        st.success("Logged out successfully.")

# --- Footer ---
st.markdown("---")
st.caption("© 2025 VulnBuster | Built with ❤️ using Streamlit & OpenAI")
