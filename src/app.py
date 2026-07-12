from fastapi import FastAPI
import joblib
import logging
import json
import pandas as pd
import time
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

# Initialize FastAPI app
app = FastAPI()

accuracy_gauge = Gauge("model_accuracy", "Accuracy of the model", ["model"])
precision_gauge = Gauge("model_precision", "Precision of the model", ["model"])
recall_gauge = Gauge("model_recall", "Recall of the model", ["model"])
f1_gauge = Gauge("model_f1_score", "F1 score of the model", ["model"])
roc_auc_gauge = Gauge("model_roc_auc", "ROC AUC of the model", ["model"])

pipeline = joblib.load("models/final_pipeline.pkl")


def load_model_metrics():
    try:
        with open("models/metrics.json", "r", encoding="utf-8") as metrics_file:
            metrics = json.load(metrics_file)
    except FileNotFoundError:
        return

    for model_name, metric_values in metrics.items():
        accuracy_gauge.labels(model=model_name).set(metric_values.get("accuracy", 0.0))
        precision_gauge.labels(model=model_name).set(metric_values.get("precision", 0.0))
        recall_gauge.labels(model=model_name).set(metric_values.get("recall", 0.0))
        f1_gauge.labels(model=model_name).set(metric_values.get("f1_score", 0.0))
        roc_auc_gauge.labels(model=model_name).set(metric_values.get("roc_auc", 0.0))


load_model_metrics()
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

# Data drift
AGE_HIST = Histogram("feature_age", "Distribution of age feature", buckets=[20, 30, 40, 50, 60, 70, 80])

# Performance degradation
REQUEST_LATENCY = Histogram("request_latency_seconds", "Latency of prediction requests")

# --- Endpoints ---


@app.post("/predict")
def predict(data: dict):
    start = time.time()
    try:
        features = data.get("features")
        X = pd.DataFrame([features], columns=feature_names)

        AGE_HIST.observe(features[0])

        y_pred = pipeline.predict(X)[0]

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
