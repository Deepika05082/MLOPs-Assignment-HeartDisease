import numpy as np
import joblib
import mlflow
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, auc, ConfusionMatrixDisplay
)
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from src.preprocessing import preprocess_data
import os

def train_and_log():
    # Get preprocessed data and preprocessor
    X_train, X_test, y_train, y_test, preprocessor = preprocess_data()
    y_train = np.array(y_train).ravel()
    y_test = np.array(y_test).ravel()

    # Logistic Regression pipeline
    log_reg = LogisticRegression(max_iter=10000, random_state=42, class_weight="balanced")
    log_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", log_reg)
    ])

    param_grid_log = {
        "model__C": [0.01, 0.1, 1, 10],
        "model__penalty": ["l2"],
        "model__solver": ["lbfgs", "saga"]
    }
    grid_log = GridSearchCV(log_pipeline, param_grid_log, cv=5, scoring="roc_auc_ovr")
    grid_log.fit(X_train, y_train)
    best_log = grid_log.best_estimator_

    # Random Forest pipeline
    rf = RandomForestClassifier(random_state=42, class_weight="balanced")
    rf_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", rf)
    ])

    param_dist_rf = {
        "model__n_estimators": [100, 200, 300],
        "model__max_depth": [None, 5, 10],
        "model__min_samples_split": [2, 5, 10],
        "model__min_samples_leaf": [1, 2, 4],
        "model__max_features": ["sqrt", "log2"]
    }
    rand_rf = RandomizedSearchCV(rf_pipeline, param_dist_rf, n_iter=10, cv=5,
                                 scoring="roc_auc_ovr", random_state=42, n_jobs=-1)
    rand_rf.fit(X_train, y_train)
    best_rf = rand_rf.best_estimator_

    os.makedirs("models", exist_ok=True)
    mlflow.end_run()
    # Evaluate and log both models
    for pipeline, name, params in [(best_log, "Logistic Regression", grid_log.best_params_),
                                   (best_rf, "Random Forest", rand_rf.best_params_)]:
        with mlflow.start_run(run_name=name):
            pipeline.fit(X_train, y_train)
            y_pred = pipeline.predict(X_test)
            y_proba = pipeline.predict_proba(X_test)

            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, average="macro", zero_division=0)
            rec = recall_score(y_test, y_pred, average="macro", zero_division=0)
            f1 = f1_score(y_test, y_pred, average="macro")
            roc = roc_auc_score(y_test, y_proba, multi_class="ovr")

            mlflow.log_param("model", name)
            mlflow.log_params(params)
            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("precision", prec)
            mlflow.log_metric("recall", rec)
            mlflow.log_metric("f1_score", f1)
            mlflow.log_metric("roc_auc", roc)

            # Save pipeline with joblib
            joblib.dump(pipeline, f"models/{name}_pipeline.pkl")

            # Log the saved pipeline as an artifact
            mlflow.log_artifact(f"models/{name}_pipeline.pkl")


            n_classes = y_proba.shape[1]

            plt.figure(figsize=(8, 6))
            for i in range(n_classes):
                fpr, tpr, _ = roc_curve(y_test == i, y_proba[:, i])
                roc_auc = auc(fpr, tpr)
                plt.plot(fpr, tpr, label=f"Class {i} (AUC = {roc_auc:.2f})")

            plt.plot([0, 1], [0, 1], "k--")
            plt.xlabel("False Positive Rate")
            plt.ylabel("True Positive Rate")
            plt.title(f"{name} ROC Curves (OvR)")
            plt.legend(loc="lower right")
            roc_path =f"eda/roc_curve_{name.replace(' ', '_')}.png"
            plt.savefig(roc_path)
            mlflow.log_artifact(roc_path)
            plt.close()

            # Confusion Matrix
            ConfusionMatrixDisplay.from_estimator(pipeline, X_test, y_test)
            plt.title(f"{name} Confusion Matrix")
            cm_path = f"eda/confusion_matrix_{name.replace(' ', '_')}.png"
            plt.savefig(cm_path)
            mlflow.log_artifact(cm_path)
            plt.close()

            # Save final pipeline
            joblib.dump(pipeline, "models/final_model.pkl")
            if name == "Random Forest":
                preprocessor.fit(X_train)
                feature_names = preprocessor.get_feature_names_out()
                importances = pipeline.named_steps["model"].feature_importances_
                indices = np.argsort(importances)[::-1][:10]

                plt.figure(figsize=(10, 6))
                plt.bar(range(len(indices)), importances[indices], align="center")
                plt.xticks(range(len(indices)), [feature_names[i] for i in indices],
                           rotation=45, ha="right")
                plt.title("Top 10 Feature Importances (Random Forest)")
                plt.tight_layout()
                plt.savefig("eda/feature_importance.png")
                mlflow.log_artifact("eda/feature_importance.png")
                plt.close()

            mlflow.end_run()  

if __name__ == "__main__":
    train_and_log()
