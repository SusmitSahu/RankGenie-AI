import ollama
import numpy as np


class GTEEmbedder:

    def __init__(self, model_name="gte-large"):
        self.model_name = model_name

    def embed(self, text):

        response = ollama.embeddings(
            model=self.model_name,
            prompt=text
        )

        embedding = response["embedding"]

        return np.array(embedding)