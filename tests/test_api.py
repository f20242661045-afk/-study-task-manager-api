def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_read_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Learn Python",
            "description": "Practice functions",
            "priority": 5,
            "due_date": "2026-08-20",
        },
    )

    assert response.status_code == 201

    created_task = response.json()

    assert created_task["title"] == "Learn Python"
    assert created_task["priority"] == 5
    assert created_task["completed"] is False

    task_id = created_task["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Learn Python"


def test_invalid_priority_is_rejected(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Invalid Task",
            "description": "",
            "priority": 9,
        },
    )

    assert response.status_code == 422


def test_update_and_complete_task(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Learn SQL",
            "description": "Practice SELECT",
            "priority": 3,
        },
    )

    task_id = create_response.json()["id"]

    update_response = client.patch(
        f"/tasks/{task_id}",
        json={
            "priority": 5,
        },
    )

    assert update_response.status_code == 200
    assert update_response.json()["priority"] == 5

    complete_response = client.patch(
        f"/tasks/{task_id}/complete"
    )

    assert complete_response.status_code == 200
    assert complete_response.json()["completed"] is True


def test_search_tasks(client):
    client.post(
        "/tasks",
        json={
            "title": "Learn Python",
            "description": "Practice loops",
            "priority": 4,
        },
    )

    client.post(
        "/tasks",
        json={
            "title": "Learn SQL",
            "description": "Practice queries",
            "priority": 3,
        },
    )

    response = client.get(
        "/tasks/search",
        params={"query": "Python"},
    )

    assert response.status_code == 200

    results = response.json()

    assert len(results) == 1
    assert results[0]["title"] == "Learn Python"


def test_priority_queue_returns_best_task(client):
    client.post(
        "/tasks",
        json={
            "title": "Lower Priority",
            "priority": 3,
            "due_date": "2026-08-10",
        },
    )

    client.post(
        "/tasks",
        json={
            "title": "High Priority Later",
            "priority": 5,
            "due_date": "2026-08-20",
        },
    )

    client.post(
        "/tasks",
        json={
            "title": "High Priority Earlier",
            "priority": 5,
            "due_date": "2026-08-15",
        },
    )

    response = client.get("/tasks/next")

    assert response.status_code == 200
    assert response.json()["title"] == "High Priority Earlier"


def test_delete_task(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Delete Me",
            "priority": 2,
        },
    )

    task_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/tasks/{task_id}"
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/tasks/{task_id}"
    )

    assert get_response.status_code == 404