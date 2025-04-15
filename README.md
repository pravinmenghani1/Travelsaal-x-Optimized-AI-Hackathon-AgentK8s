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

```text
Action: DummyTool
Action Input: {"metric": "node_cpu_utilization"}
Observation: Simulated tool output for input: {'metric': 'node_cpu_utilization'} 


### 4. PDF Report Generation
After all user inputs are collected and analyzed, a Markdown-style report is created and visualized using Streamlit, and exported as a PDF (via libraries like pdfkit or reportlab, depending on setup).

🌐 Web UI (Streamlit)
The frontend is built using Streamlit, allowing users to:

Fill in structured details about their EKS environment

Submit input for analysis

View identified risks and recommendations

Download the PDF report

Example UI workflow:


from agents.agentk8s import AgentK8s
from agents.tools.dummy_tool import DummyTool

agent = AgentK8s(tools=[DummyTool()])
response = agent("Our EKS nodes go into NotReady, and we use shared IAM roles...")
