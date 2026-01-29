def test_login_invalid_credentials(client):
    res = client.post(
        "/auth/login",
        data={
            "username": "fake@test.com",  
            "password": "wrong"
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )
    assert res.status_code == 401



def test_login_missing_fields(client):
    res = client.post("/auth/login", json={})
    assert res.status_code == 422
