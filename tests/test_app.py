from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_predict_endpoint():
    response = client.post("/predict", json={"features":[63,1,1,145,233,1,0,150,0,2.3,0,0,1]})
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probabilities" in data

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "request_count_total" in response.text
