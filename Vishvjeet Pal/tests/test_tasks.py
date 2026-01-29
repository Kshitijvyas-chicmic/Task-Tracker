def test_create_task_without_token(client):
    res = client.post("/tasks/", json={
        "title": "Test Task",
        "description": "Test",
        "priority": "high"
    })
    assert res.status_code in (401, 403)


def test_list_tasks_without_token(client):
    res = client.get("/tasks/")
    assert res.status_code in (401, 403)
