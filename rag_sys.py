import random
import httpx
import ollama

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage



from langchain_chroma import Chroma
from openai import OpenAI

import ollama


class GTEEmbedder:

    def __init__(self, model_name="gte-large"):
        self.model_name = model_name

    def embed_query(self, text):
        return ollama.embeddings(
            model=self.model_name,
            prompt=text
        )["embedding"]

    def embed_documents(self, texts):
        return [
            ollama.embeddings(
                model=self.model_name,
                prompt=t
            )["embedding"]
            for t in texts
        ]

def generate_dummy_alerts(n=20):

    alerts = []

    for _ in range(n):

        alert = {
            "description": random.choice([
                "High CPU utilization detected on compute node.",
                "Disk throughput unusually high indicating heavy IO activity.",
                "Packet loss observed in network communication.",
                "Large number of active connections detected on the server.",
                "Free storage critically low on storage volume."
            ]),
            "features": {
                "CPU_utilization": round(random.uniform(0.1, 0.95), 2),
                "num_running_processes": random.randint(50, 400),
                "IO_operations": random.randint(500, 5000),
                "disk_throughput": round(random.uniform(10, 200), 2),
                "free_storage": round(random.uniform(0.05, 0.8), 2),
                "packet_loss": round(random.uniform(0.0, 0.2), 3),
                "active_connections": random.randint(50, 1000)
            },
            "severity": random.randint(1,5),
            "risk": "System performance degradation may occur if the issue persists.",
            "resolution": "Investigate system load, restart services, or scale infrastructure."
        }

        alerts.append(alert)

    return alerts

def alert_to_text(alert):

    features = "\n".join(
        [f"{k}: {v}" for k, v in alert["features"].items()]
    )

    text = f"""
Description:
{alert['description']}

Features:
{features}

Severity: {alert.get('severity','')}
Risk: {alert.get('risk','')}
Resolution: {alert.get('resolution','')}
"""

    return text.strip()


def run_alert_rag(current_alert, severity, api_key, db_path="./alert_db"):

    # Fix SSL issue
    http_client = httpx.Client(verify=False)

    # Custom embeddings
    # embedding_model = OpenAIEmbeddings(
    #     base_url="https://genailab.tcs.in",
    #     model="azure/genailab-maas-text-embedding-3-large",
    #     api_key=api_key,
    #     http_client=http_client
    # )

    embedding_model = GTEEmbedder()

    # Vector DB
    vectorstore = Chroma(
        collection_name="alerts",
        embedding_function=embedding_model,
        persist_directory=db_path
    )

    # Populate DB if empty
    if vectorstore._collection.count() == 0:

        print("Initializing vector DB with dummy alerts...")

        historical_data = generate_dummy_alerts(25)

        docs = [alert_to_text(a) for a in historical_data]

        vectorstore.add_texts(docs)
        vectorstore.persist()

        print("Vector DB initialized.")

    # Query
    query_text = alert_to_text(current_alert)

    results = vectorstore.similarity_search(query_text, k=3)

    context = "\n\n".join([r.page_content for r in results])

    # LLM
    gpt_4o = ChatOpenAI(
        model="azure/genailab-maas-gpt-4o-mini",
        base_url="https://genailab.tcs.in",
        api_key="sk-nNEWfrlxa6GySU_4vPaLkQ",
        http_client=http_client
    )

    system_prompt = """
You are an intelligent AI system that analyzes infrastructure alerts.
Explain the severity score and generate risk and resolution.
Return ONLY valid JSON.
"""

    user_prompt = f"""
Current Alert:
{query_text}

ML Predicted Severity: {severity}

Similar Historical Alerts:
{context}

Return JSON:

{{
"description": "...",
"features": {{...}},
"severity": int,
"risk": "...",
"resolution": "...",
"rationale": "..."
}}
"""

    response = gpt_4o.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
    )

    return response.content

current_alert = {
    "description": "CPU utilization extremely high on compute node.",
    "features": {
        "CPU_utilization": 0.91,
        "num_running_processes": 210,
        "IO_operations": 3200,
        "disk_throughput": 130,
        "free_storage": 0.12,
        "packet_loss": 0.02,
        "active_connections": 780
    }
}

severity = 4

result = run_alert_rag(
    current_alert=current_alert,
    severity=severity,
    api_key="sk-nNEWfrlxa6GySU_4vPaLkQ"
)

print(result)