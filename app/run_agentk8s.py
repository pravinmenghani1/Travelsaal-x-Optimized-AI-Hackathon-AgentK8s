# app/run_agentk8s.py

import streamlit as st
import os
import sys

# Get the absolute path of the current file and add project root to Python path
current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Debug information
print(f"Current file: {current_file}")
print(f"Current directory: {current_dir}")
print(f"Project root: {project_root}")
print(f"Python path: {sys.path}")
print(f"Directory contents: {os.listdir(project_root)}")

# Function to validate OpenAI API key format
def validate_api_key(api_key):
    """Basic validation of API key format"""
    if not api_key.startswith('sk-'):
        return False
    if len(api_key) < 20:
        return False
    return True

# Function to check if API key is set
def check_openai_api_key():
    """Check if OpenAI API key is set and valid"""
    if not st.session_state.get("OPENAI_API_KEY"):
        st.error("Please enter your OpenAI API key in the sidebar!")
        st.stop()
    os.environ["OPENAI_API_KEY"] = st.session_state.OPENAI_API_KEY

# Page configuration - this should be the first Streamlit command
st.set_page_config(page_title="AgentK8s – EKS Operational Review", layout="wide")

# Import required modules
try:
    from agents.agentk8s import AgentK8s
    from agents.pdf_generator import generate_pdf
    from openai import OpenAIError
except ImportError as e:
    st.error(f"Import Error: {str(e)}")
    st.error(f"Current working directory: {os.getcwd()}")
    st.error(f"Contents of current directory: {os.listdir()}")
    if os.path.exists(os.path.join(project_root, 'agents')):
        st.error(f"Contents of agents directory: {os.listdir(os.path.join(project_root, 'agents'))}")
    raise

# Sidebar for API key configuration
with st.sidebar:
    st.markdown("## Configuration")
    api_key = st.text_input(
        "Enter your OpenAI API key",
        type="password",
        placeholder="sk-...",
        help="Get your API key from https://platform.openai.com/account/api-keys",
        value=st.session_state.get("OPENAI_API_KEY", "")
    )
    
    if api_key:
        if not validate_api_key(api_key):
            st.sidebar.error("Invalid API key format. It should start with 'sk-'")
            st.stop()
        with st.spinner("Validating API key..."):
            st.session_state.OPENAI_API_KEY = api_key
    
    # API key instructions and disclaimers...
    st.markdown("""
    ### How to get an OpenAI API key
    1. Go to [OpenAI API Keys](https://platform.openai.com/account/api-keys)
    2. Create an account or sign in
    3. Create a new secret key
    4. Copy and paste it here
    """)

    if 'OPENAI_API_KEY' in st.session_state:
        st.info("✅ API key is set for this session")
        if st.button("Clear API Key"):
            del st.session_state.OPENAI_API_KEY
            st.experimental_rerun()

# Check for API key before proceeding
check_openai_api_key()

# Main app content
st.title("AgentK8s - EKS Operational Review Agent 🤖")
st.markdown("Provide details across all areas to generate a comprehensive report.")

# Rest of your code (form, submission handling, etc.) remains the same...
