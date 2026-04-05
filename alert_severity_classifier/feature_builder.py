import numpy as np
from config import NUMERIC_FEATURES


def build_feature_vector(embedder, df):

    features = []

    for _, row in df.iterrows():

        text_embedding = embedder.embed(row["description"])

        numeric = row[NUMERIC_FEATURES].values.astype(float)

        combined = np.concatenate([text_embedding, numeric])

        features.append(combined)

    return np.array(features)