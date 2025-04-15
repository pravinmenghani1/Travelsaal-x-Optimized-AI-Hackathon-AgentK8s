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

