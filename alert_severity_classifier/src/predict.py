import joblib
import numpy as np
import json

from embedder import GTEEmbedder
from data_loader import load_test_data
from feature_builder import build_feature_vector
from config import TEST_FILE, MODEL_PATH, SCALER_PATH


def predict():

    df = load_test_data(TEST_FILE)

    embedder = GTEEmbedder()

    X = build_feature_vector(embedder, df)

    scaler = joblib.load(SCALER_PATH)
    model = joblib.load(MODEL_PATH)

    X = scaler.transform(X)

    preds = model.predict(X)

    df["predicted_severity"] = preds

    output = df.to_dict(orient="records")

    with open("predictions.json", "w") as f:
        json.dump(output, f, indent=4)

    print("Predictions saved to predictions.json")


if __name__ == "__main__":
    predict()