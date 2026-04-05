from src.train import train
from src.predict import predict


if __name__ == "__main__":

    print("Training model...")
    train()

    print("Running predictions...")
    predict()