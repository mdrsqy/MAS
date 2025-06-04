import joblib
import os

def load_model(path: str):
    if not path.endswith('.pkl'):
        raise ValueError("Only .pkl files are supported.")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found at: {path}")

    try:
        model = joblib.load(path)
        print(f"Model loaded successfully from {path}")
        return model
    except Exception as e:
        raise RuntimeError(f"Error loading model from {path}: {e}")