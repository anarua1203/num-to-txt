import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_num_to_english():
    response = client.get("/num_to_english?number=12&lang=en")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "num_in_english": "twelve"}

def test_post_num_to_english():
    data = {"number": 12}
    response = client.post("/num_to_english", json=data)
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "num_in_english": "twelve"}

def test_get_num_to_english_custom_lang():
    response = client.get("/num_to_english?number=12&lang=es")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "num_in_english": "doce"}

def test_invalid_number():
    response = client.get("/num_to_english?number=invalid")
    assert response.status_code == 500
    # assert "value is not a valid integer" in response.text

def test_missing_number():
    response = client.get("/num_to_english")
    assert response.status_code == 422
    # assert "field required" in response.text

def test_post_missing_number():
    data = {"key": "value"}
    response = client.post("/num_to_english", json=data)
    assert response.status_code == 422
    # assert "field required" in response.text