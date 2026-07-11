from fastapi import FastAPI
import joblib
import logging
import pandas as pd
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

# Initialize FastAPI app
app = FastAPI()
pipeline = joblib.load("models/final_pipeline.pkl")
feature_names = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"
]

# Configure logging
logging.basicConfig(level=logging.INFO)

# --- Monitoring Metrics ---
# Request counter
REQUEST_COUNT = Counter("request_count_total", "Total prediction requests")

# Model failures
FAILED_PREDICTIONS = Counter("failed_predictions_total", "Number of failed predictions")

# Data drift (example: age feature distribution)
AGE_HIST = Histogram("feature_age", "Distribution of age feature", buckets=[20, 30, 40, 50, 60, 70, 80])

# Performance degradation (latency)
REQUEST_LATENCY = Histogram("request_latency_seconds", "Latency of prediction requests")

# --- Endpoints ---


@app.post("/predict")
def predict(data: dict):
    start = time.time()
    try:
        features = data.get("features")
        X = pd.DataFrame([features], columns=feature_names)

        # Example: observe age feature (first column)
        AGE_HIST.observe(features[0])

        y_pred = pipeline.predict(X)[0]

        # Map probabilities to class labels
        class_labels = {
            0: "No disease",
            1: "Mild disease",
            2: "Moderate disease",
            3: "Severe disease",
            4: "Very severe disease"
        }

        probs = pipeline.predict_proba(X)[0]
        probabilities = {class_labels[label]: float(prob) for label, prob in zip(pipeline.classes_, probs)}

        # Monitoring updates
        REQUEST_COUNT.inc()
        REQUEST_LATENCY.observe(time.time() - start)

        return {
            "prediction": class_labels[int(y_pred)],
            "probabilities": probabilities
        }
    except Exception:
        FAILED_PREDICTIONS.inc()
        raise


@app.get("/metrics")
def metrics():
    """Prometheus metrics endpoint."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
