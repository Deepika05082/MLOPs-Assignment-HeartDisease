from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_predict_endpoint():
    response = client.post("/predict", json={"features": [63, 1, 1, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1]})
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probabilities" in data


def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "request_count_total" in response.text


# { "features": [44,1,1,120,263,0,1,173,0,0.0,2,0,3] }--no
# { "features": [54,0,2,140,239,0,0,160,0,1.2,1,0,2] }
# { "features": [62,1,3,130,297,0,1,120,1,2.5,2,2,3] }
# { "features": [37,0,1,120,215,0,0,170,0,0.0,1,0,2] }
# { "features": [50,1,0,150,250,1,2,140,1,1.8,2,1,7] }
# { "features": [65,0,3,160,310,0,1,108,1,3.0,3,2,6] }--moderate
# { "features": [52, 1, 0, 145, 260, 1, 0, 170, 0, 1.0, 2, 0, 3] }
# { "features": [70, 0, 3, 160, 310, 1, 2, 108, 1, 3.5, 3, 2, 6] }--sever
