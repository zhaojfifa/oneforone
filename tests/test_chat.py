import os, requests
BASE = os.getenv("BASE_URL", "http://127.0.0.1:10000")
def test_health():
    r = requests.get(f"{BASE}/health")
    assert r.status_code == 200
    assert r.json().get("ok") is True
