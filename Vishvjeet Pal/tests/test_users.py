def test_create_user_unauthorized(client):
    res = client.post("/users/", json={
        "name": "Test User",
        "email": "test@x.com",
        "password": "1234",
        "role_name": "employee"
    })
    assert res.status_code in (401, 403)
