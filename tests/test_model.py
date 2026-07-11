import joblib


def test_model_load():
    model = joblib.load("models/final_pipeline.pkl")
    assert model is not None
