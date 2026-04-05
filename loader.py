import json
from pathlib import Path
from alert_severity_classifier.src.predict import predict_severity

# ---------------------------------------------------
# Project Paths
# ---------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

OPEN_ALERTS_PATH = BASE_DIR / "dataset" / "open_alerts_dataset_10.json"
CLOSED_ALERTS_PATH = BASE_DIR / "dataset" / "historical_dataset_450.json"

RAG_ALERTS_PATH = BASE_DIR / "dataset" / "output_rag_10.json"



# ---------------------------------------------------
# Generic JSON Loader
# ---------------------------------------------------

def load_json(path):

    if not path.exists():
        print(f"File not found: {path}")
        return []

    with open(path, "r") as f:
        data = json.load(f)

    return data


# ---------------------------------------------------
# Load Alerts (Open + Closed)
# ---------------------------------------------------

def load_alerts():

    open_alerts = load_json(OPEN_ALERTS_PATH)
    closed_alerts = load_json(CLOSED_ALERTS_PATH)
    rag_alerts = load_json(RAG_ALERTS_PATH)

    id_to_risk = {}
    id_to_resol = {}
    id_to_rationale = {}
    for op in rag_alerts:
        id_to_risk[int(op["id"])] = op["risk"]
        id_to_resol[int(op["id"])] = op["resolution"]
        id_to_rationale[int(op["id"])] = op["rationale"]

    id_to_severity = predict_severity()


    # Tag alert status
    for alert in open_alerts:
        alert["status"] = "open"
        alert["risk"] = id_to_risk[alert["id"]]
        alert["resolution"] = id_to_resol[alert["id"]]
        alert["rationale"] = id_to_rationale[alert["id"]]

        
        alert["severity"] = id_to_severity[alert["id"]]

    for alert in closed_alerts:
        alert["status"] = "closed"

    alerts = open_alerts + closed_alerts

    return alerts