# RankGenie-AI

A GenAI-driven alert prioritization assistant designed to help performance engineers efficiently manage and respond to infrastructure alerts.
Modern monitoring systems generate high volumes of alerts, making manual prioritization:
❌ Inconsistent
❌ Subjective
❌ Error-prone

This solution leverages LLMs + Vector Search (RAG) to:
Rank alerts by severity and impact
Provide context-aware explanations
Suggest risk and resolution steps
  
🎯 Problem Statement

Performance monitoring systems generate numerous alerts, making it difficult to identify critical issues quickly.
Engineers often struggle with alert fatigue, leading to delayed responses and missed incidents.
💡 Solution
A Retrieval-Augmented Generation (RAG) based assistant that:
✅ Stores historical alerts in a vector database
✅ Retrieves similar past alerts
✅ Uses an LLM to:
Explain severity
Generate risk assessment
Suggest resolutions
Provide rationale

                ┌──────────────────────┐
                │  Current Alert Input │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │  Feature Extraction  │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │ Vector DB (Chroma)   │
                │  (Historical Alerts) │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │ Similarity Search    │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │   LLM (GPT-4o-mini)  │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │ Ranked Output + JSON │
                └──────────────────────┘

⚙️ Tech Stack
Python
LangChain
ChromaDB (Vector Store)
Ollama (Local Embeddings - GTE Large)
OpenAI / Azure GPT (LLM)
HTTPX

🚀 Features
🔍 Semantic Alert Search using embeddings
🤖 LLM-powered reasoning
📊 Severity explanation & justification
⚠️ Risk assessment generation
🛠️ Resolution recommendations
🧪 Synthetic data generation for testing
