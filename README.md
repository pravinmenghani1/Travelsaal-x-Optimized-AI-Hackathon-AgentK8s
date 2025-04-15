# 🧠 AgentK8s - EKS Operational Review Agent

**AgentK8s** is an AI-powered assistant built on the [AgentPro](https://github.com/traversaal/agentpro) framework. It performs an operational review of your **Amazon EKS (Elastic Kubernetes Service)** cluster and generates a **prescriptive action plan** with categorized recommendations to improve your environment.

The assistant interacts with users via a **web-based UI (Streamlit)** and produces a **PDF report** detailing identified risks and recommended best practices.

---

## 🚀 Features

- Conversational interface for collecting EKS environment context
- AI reasoning engine using OpenAI or OpenRouter models
- Custom tools integration for advanced diagnostics
- Risk identification across EKS pillars:
  - Cluster Health
  - Cost Optimization
  - Security
  - Monitoring
  - CI/CD
  - Windows Containers
- Generates a report with:
  - ⚠️ Risks
  - ✅ Recommendations
  - Categorized by: Short-Term, Medium-Term, Long-Term
- Report visualization and export as **PDF**

---

## 📁 Project Structure


AgentPro/ ├── agents/ │ ├── agentk8s.py # Main AI agent logic using AgentPro-style REACT loop │ └── tools/ │ ├── base.py # Base Tool class │ └── dummy_tool.py # Example tool for testing agent actions ├── app/ │ └── streamlit_app.py # Web UI built with Streamlit ├── reports/ │ └── output.pdf # Generated PDF report (optional output folder) └── README.md



---

## 🧠 How It Works

### 1. Agent Architecture (REACT Pattern)
`AgentK8s` is built using a reasoning loop inspired by [AgentPro](https://github.com/traversaal/agentpro)'s architecture. It follows this structure:


Question ➝ Thought ➝ Action ➝ Action Input ➝ Observation ➝ ... ➝ Final Answer



This enables multi-step reasoning before arriving at a final recommendation.

### 2. System Prompt for EKS Analysis
The system prompt guides the agent to:
- Ask intelligent follow-up questions
- Identify operational risks
- Categorize recommendations into:
  - **Short-Term (0–3 months)**
  - **Medium-Term (3–6 months)**
  - **Long-Term (6–18 months)**

### 3. Tool Integration
The agent supports calling custom tools (e.g., metrics scanners, cost analyzers) using the `Tool` base class. You can plug in new tools by extending the `Tool` interface.

Example tool call from the agent:



### 4. PDF Report Generation
After all user inputs are collected and analyzed, a Markdown-style report is created and visualized using Streamlit, and exported as a PDF (via libraries like pdfkit or reportlab, depending on setup).

### 🌐 Web UI (Streamlit)
The frontend is built using Streamlit, allowing users to:

Fill in structured details about their EKS environment

Submit input for analysis

View identified risks and recommendations

Download the PDF report

Example UI workflow:

---
from agents.agentk8s import AgentK8s
from agents.tools.dummy_tool import DummyTool

agent = AgentK8s(tools=[DummyTool()])
response = agent("Our EKS nodes go into NotReady, and we use shared IAM roles...")

📄 Sample Output

### EKS Operational Report

🚨 Risks Identified

**Cluster Health**
- Nodes frequently enter NotReady state due to missing health checks

**Security**
- IAM roles are shared, violating least privilege principles

✅ Recommendations

**Short-Term**
- Configure node health check probes
- Implement IAM roles for service accounts (IRSA)

**Medium-Term**
- Set up PodSecurityPolicies or use OPA/Gatekeeper

**Long-Term**
- Audit all IAM permissions and rotate keys periodically

🛠️ Setup & Run
1. Clone the repo
bash
Copy
Edit
git clone https://github.com/your-org/agentk8s.git
cd agentk8s
2. Set up environment
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Set environment variables (for OpenRouter or OpenAI):

bash
Copy
Edit
export OPENROUTER_API_KEY=your_key
export MODEL_NAME=gpt-4o-mini  # or gpt-3.5-turbo
3. Run the Streamlit app
bash
Copy
Edit
PYTHONPATH=. streamlit run app/streamlit_app.py
📦 Extending the Agent
You can create new tools by extending the Tool class in agents/tools/base.py. For example:

python
Copy
Edit
class MyTool(Tool):
    name = "K8sMetricsTool"

    def get_tool_description(self):
        return "Fetches real-time metrics from the EKS cluster."

    def run(self, input_data):
        # logic to fetch from CloudWatch or Prometheus
        return result
Then plug it into AgentK8s:

python
Copy
Edit
agent = AgentK8s(tools=[MyTool()])
🧪 Debugging Tips
Add st.write(agent.messages) in the Streamlit app to view the agent's reasoning.

Make sure PYTHONPATH is correctly set to resolve local imports.

Use descriptive prompts. Example:

vbnet
Copy
Edit
“Our EKS workloads often restart due to OOMKilled. We're not using resource limits or liveness probes.”
🧩 Dependencies
openai or openrouter

streamlit

pdfkit or reportlab (for PDF generation)

re, json, os, collections

📝 License
MIT License © 2025 [Your Company or Name]

🤝 Contributing
PRs are welcome! Add your own tools, metrics visualizations, or integrations (e.g., Slack, Prometheus, ArgoCD).

