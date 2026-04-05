import json
import pandas as pd
from config import NUMERIC_FEATURES


def load_training_data(file_path):

    with open(file_path) as f:
        data = json.load(f)

    rows = []

    for item in data:

        row = {
            "description": item["description"],
            "severity": item["severity"]
        }

        for feature in NUMERIC_FEATURES:
            row[feature] = item["features"][feature]

        rows.append(row)

    return pd.DataFrame(rows)


def load_test_data(file_path):

    with open(file_path) as f:
        data = json.load(f)

    rows = []

    for item in data:

        row = {"id": item["id"], "description": item["description"]}

        for feature in NUMERIC_FEATURES:
            row[feature] = item["features"][feature]

        rows.append(row)

    return pd.DataFrame(rows)