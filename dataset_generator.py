from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import json
from datetime import datetime
import re

from models import gpt_4o

# ----- SYSTEM PROMPT -----
system_prompt = """
You are a synthetic data generator for developing a performance engineering alert prioritization assistant. You strictly generate the data in the following JSON format. Here, the following JSON structure represents data about 1 alert.

{
    "description": <textual description of the alert using maximum of 4 sentences>,
    "features": {
        "CPU_utilization": <float between 0 and 1>,
        "num_running_processes": <number of running processes>,
        "IO_operations": <nmumber of input/output operations per second>,
        "disk_throughput": <float indicating MB per second>,
        "free_storage": <float between 0 and 1 indicating fraction of free storage left>,
        "packet_loss": <float between 0 and 1 indicating fraction of packets loss>,
        "active_connections": <number of active connections>       
    },
    "severity": <number between 1 (low) to 5 (high) indicating level of severity>,
    "risk": <ramifications if not handled in 1 or 2 sentences>,
    "resolution": <description of potential resolutions in maximum of 4 sentences>
}

Response format:
[
    {<alert1>},
    {<alert2>},
    ...
]
"""

# ----- USER PROMPT -----
user_prompt = """
Generate synthetic data for a performance engineering alerts for monitoring a huge cloud infrastructure system. Each alert description should clearly mention the name/ID of one or more affected components/nodes/servers and also elaborate the issue in up to 4 sentences. Each alert has to be represented in a structured JSON format. Generate 10 alerts which should be diverse in their severity levels and should cover diverse set of issues.
"""

# Invoke model
response = gpt_4o.invoke(
    [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
)

# Raw output
# print("Raw Output:\n", response.content)

# Parse JSON safely
try:
    pattern_1 = re.compile(r"^[^\[]*\[")
    pattern_2 = re.compile(r"\][^\]]*$")
    content = response.content
    content = pattern_1.sub("[", content)
    content = pattern_2.sub("]", content)

    print("Processed output:", content)
    dataset = json.loads(content)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"dataset_gpt_4o_{timestamp}.json"
    with open(file_name, mode="w") as f:
        json.dump(dataset, f, indent=4)
    print("File saved as", file_name)
    # print("\nParsed JSON:\n", dataset)
except Exception as e:
    print("\nJSON parsing failed:", e)
