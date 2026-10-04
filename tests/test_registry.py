from fastapi.testclient import TestClient
from exptrack.main import app
from exptrack import registry

client = TestClient(app)


def setup_function():
    registry.CHAMPION = next(iter(registry.MODELS))


def test_promote():
    client.post("/models", json={"name": "candidate", "version": "2", "metrics": {"auc": 0.9}})
    payload = client.post("/promote", json={"name": "candidate"}).json()
    assert payload["champion"] == "candidate"
    assert payload["applied"] is False
    assert client.get("/champion").json()["champion"] == "candidate"
