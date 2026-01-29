def test_audit_logs_protected(client):
    res = client.get("/activity-logs/")
    assert res.status_code in (401, 403)
