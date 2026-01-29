def test_protected_route_requires_auth(client):
    res = client.get("/users/")
    assert res.status_code in (401, 403)
