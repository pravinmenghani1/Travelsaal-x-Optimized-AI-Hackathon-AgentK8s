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

