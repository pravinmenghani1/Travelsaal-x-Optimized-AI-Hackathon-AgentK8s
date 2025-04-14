# app/run_agentk8s.py

import streamlit as st
from agents.agentk8s import AgentK8s
from agents.pdf_generator import generate_pdf

st.set_page_config(page_title="AgentK8s – EKS Operational Review", layout="wide")
st.title("AgentK8s - EKS Operational Review Agent 🤖")
st.markdown("Provide details across all areas to generate a comprehensive report.")

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
    else:
        st.warning("Please provide details in at least one section.")
