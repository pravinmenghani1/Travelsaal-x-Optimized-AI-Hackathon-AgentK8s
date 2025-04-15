# app/run_agentk8s.py

import streamlit as st
import os
import sys
from agents.agentk8s import AgentK8s
from agents.pdf_generator import generate_pdf
from openai import OpenAIError
# app/run_agentk8s.py

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Now try to import from agents
try:
    from agents.agentk8s import AgentK8s
    from agents.pdf_generator import generate_pdf
except ImportError as e:
    st.error(f"Failed to import agents module: {str(e)}")
    st.error(f"Current directory: {os.getcwd()}")
    st.error(f"Python path: {sys.path}")
    raise

from openai import OpenAIError

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

# Page configuration
st.set_page_config(page_title="AgentK8s – EKS Operational Review", layout="wide")

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
    
    st.markdown("""
    ### How to get an OpenAI API key
    1. Go to [OpenAI API Keys](https://platform.openai.com/account/api-keys)
    2. Create an account or sign in
    3. Create a new secret key
    4. Copy and paste it here
    
    Note: Your API key is only stored temporarily in this session.
    """)
    
    st.markdown("""
    ### Important Notes:
    - Your API key is never stored permanently
    - Each request to OpenAI's API will use credits from your account
    - Estimated cost per review: ~$0.05-0.10
    - Make sure you have sufficient credits in your OpenAI account
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

try:
    agent = AgentK8s()
    user_answers = {}

    with st.form("eks_review_form"):
        st.subheader("💡 Cluster Health")
        user_answers["cluster_health"] = st.text_area(
            "Cluster Status, Node Status, Scheduling issues, etc.",
            value="We have multiple nodes frequently going NotReady. Some pods are stuck in Pending state due to insufficient memory on nodes."
        )

        st.subheader("💸 Cost Optimization")
        user_answers["cost_optimization"] = st.text_area(
            "Cost concerns, unused resources, right-sizing opportunities.",
            value="There are several underutilized EC2 instances. Cluster autoscaler is not configured. Spot instances are not being used."
        )

        st.subheader("🔐 Security")
        user_answers["security"] = st.text_area(
            "IAM roles, secrets management, network policies, etc.",
            value="No network policies are defined. IAM roles are shared across services. Secrets are stored in plain config maps."
        )

        st.subheader("📈 Monitoring")
        user_answers["monitoring"] = st.text_area(
            "Tooling, dashboards, alerts, metrics setup.",
            value="We use Prometheus and Grafana. Alerts are configured but there are no alerts for disk or memory pressure."
        )

        st.subheader("⚙️ CI/CD")
        user_answers["cicd"] = st.text_area(
            "Deployment frequency, pipeline tools, rollback strategy.",
            value="GitHub Actions is used for CI/CD. Rollbacks are manual. There is no canary or blue/green deployment strategy."
        )

        st.subheader("🧩 Others")
        user_answers["others"] = st.text_area(
            "Kubernetes version, architecture, special needs (e.g. Windows containers).",
            value="Running EKS version 1.22. Planning to migrate to 1.28. Considering Windows containers support for legacy workloads."
        )

        submitted = st.form_submit_button("Run AgentK8s")

    if submitted:
        if any(user_answers.values()):
            with st.spinner("Analyzing your EKS setup..."):
                try:
                    for key, answer in user_answers.items():
                        if answer:
                            agent.add_user_message(f"{key.replace('_', ' ').capitalize()}: {answer}")

                    final_output = agent("""
                    Please analyze the provided information and return a prescriptive action plan for improving EKS operations.

                    For each area (Cluster Health, Cost Optimization, Security, Monitoring, CI/CD, Others), list:
                    - Risk: <summary of one or more risks>
                    - Recommendation: <summary of one or more recommendations>

                    Structure your output clearly using 'Risk:' and 'Recommendation:' tags so it can be extracted.
                    """)
                    report = agent.generate_prescriptive_report()

                    st.markdown(report)

                    try:
                        pdf_file = generate_pdf(report)
                        with open(pdf_file, "rb") as f:
                            st.download_button("📄 Download PDF Report", data=f, file_name=pdf_file)
                    except Exception as e:
                        st.error(f"PDF generation failed: {str(e)}")

                except OpenAIError as e:
                    st.error(f"OpenAI API Error: {str(e)}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {str(e)}")
        else:
            st.warning("Please provide details in at least one section.")

except OpenAIError as e:
    st.error(f"OpenAI API Error: {str(e)}")
    if "API key" in str(e):
        st.error("Invalid API key. Please check your API key in the sidebar and try again.")
except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")

# Add disclaimer at the bottom
st.sidebar.markdown("""
---
### Disclaimer
This application uses your OpenAI API key to generate content. 
By using this app, you acknowledge that:
- You are responsible for any charges incurred
- Your API key is used only for this session
- No data is stored permanently
""")
