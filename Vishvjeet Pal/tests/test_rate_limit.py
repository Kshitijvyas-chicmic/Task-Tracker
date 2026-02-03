from core.utils.rate_limiter import global_limiter


def test_rate_limit_exceeded(client):
    global_limiter.storage.clear()

    for _ in range(5):
        r = client.get("/debug/ratelimit")
        assert r.status_code == 200

    r = client.get("/debug/ratelimit")
    assert r.status_code == 429
    assert r.json().get("detail") == "Rate limit exceeded"
