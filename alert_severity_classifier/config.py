MODEL_NAME = "ollama/gte-large"

NUMERIC_FEATURES = [
    "CPU_utilization",
    "num_running_processes",
    "IO_operations",
    "disk_throughput",
    "free_storage",
    "packet_loss",
    "active_connections"
]

TRAIN_FILE = "data/train.json"
TEST_FILE = "data/test.json"

MODEL_PATH = "models/severity_model.pkl"
SCALER_PATH = "models/scaler.pkl"