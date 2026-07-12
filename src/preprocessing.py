from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import os
import matplotlib.pyplot as plt
import seaborn as sns
import mlflow
import numpy as np


def preprocess_data(test_size=0.2, random_state=42):
    # Fetch dataset
    heart_disease = fetch_ucirepo(id=45)
    X = heart_disease.data.features
    y = heart_disease.data.targets

    # Identify categorical and numeric columns
    categorical_cols = ["sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal"]
    numeric_cols = [col for col in X.columns if col not in categorical_cols]

    # Define transformers
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])


    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_cols),
            ("cat", categorical_transformer, categorical_cols)
        ]
    )

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # --- Exploratory Data Analysis (EDA) ---
    os.makedirs("eda", exist_ok=True)

    # 1. Class Distribution
    plt.figure(figsize=(6, 6))
    y_counts = np.bincount(y_train.values.ravel())
    plt.pie(y_counts, labels=np.unique(y_train), autopct='%1.1f%%')
    plt.title("Class Distribution (Train)")
    plt.savefig("eda/class_distribution_pie.png")
    mlflow.log_artifact("eda/class_distribution_pie.png")
    plt.close()

    plt.figure(figsize=(6, 4))
    plt.bar(np.unique(y_train), y_counts)
    plt.title("Class Distribution (Train)")
    plt.xlabel("Classes")
    plt.ylabel("Count")
    plt.savefig("eda/class_distribution_bar.png")
    mlflow.log_artifact("eda/class_distribution_bar.png")
    plt.close()

    # 2. Age Distribution
    if "age" in X_train.columns:
        plt.figure(figsize=(8, 6))
        plt.hist(X_train["age"], bins=20, color="skyblue", edgecolor="black")
        plt.title("Age Distribution")
        plt.xlabel("Age")
        plt.ylabel("Frequency")
        plt.savefig("eda/age_distribution.png")
        mlflow.log_artifact("eda/age_distribution.png")
        plt.close()

    # 3. Correlation Heatmap
    corr = X_train.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, cmap="coolwarm", annot=False)
    plt.title("Feature Correlation Heatmap")
    plt.savefig("eda/correlation_heatmap.png")
    mlflow.log_artifact("eda/correlation_heatmap.png")
    plt.close()

    # 4. Box Plots for Outliers 
    for col in numeric_cols[:5]:
        plt.figure(figsize=(6, 4))
        sns.boxplot(x=X_train[col])
        plt.title(f"Box Plot - {col}")
        plt.savefig(f"eda/boxplot_{col}.png")
        mlflow.log_artifact(f"eda/boxplot_{col}.png")
        plt.close()

    return X_train, X_test, y_train, y_test, preprocessor
