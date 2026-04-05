import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

from embedder import GTEEmbedder
from data_loader import load_training_data
from feature_builder import build_feature_vector
from config import TRAIN_FILE, MODEL_PATH, SCALER_PATH


def train():

    df = load_training_data(TRAIN_FILE)

    embedder = GTEEmbedder()

    X = build_feature_vector(embedder, df)
    y = df["severity"].values

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    print("MSE:", mean_squared_error(y_test, preds))
    print("MAE:", mean_absolute_error(y_test, preds))

    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    print("Model saved")


if __name__ == "__main__":
    train()