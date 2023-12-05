import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

response = client.get("/num_to_english?number=&lang=es")
print(response)
print(response.status_code)
print(response.json())

print(response.content)