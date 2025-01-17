from tests.conftest import setup_db, test_client


def test_contribute(test_client, setup_db):
    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "test@tester.com", "password": "test"},
    )

    token = response.json().get("access_token")
    assert response.status_code == 200
    assert token
    assert response.json().get("token_type") == "bearer"

    response = test_client.post(
        "/projects",
        json={
            "title": "test",
            "description": "test",
            "goal_amount": 1,
            "deadline": "2026-01-01T12:00:00.000Z",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    id = response.json().get("id")
    assert response.status_code == 200
    assert response.json().get("title") == "test"
    assert response.json().get("description") == "test"
    assert response.json().get("goal_amount") == "1"
    assert id
    assert response.json().get("deadline")
    assert response.json().get("created_at")

    response = test_client.post(
        f"/projects/{id}/contribute",
        json={"amount": 1},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json().get("amount") == "1"
    assert response.json().get("user")
    assert response.json().get("project")
    assert response.json().get("created_at")


def test_contribute_unauthenticated(test_client, setup_db):
    response = test_client.post(f"/projects/{id}/contribute", json={"amount": 1})

    assert response.status_code == 401
    assert response.json().get("detail") == "Not authenticated"


def test_contribute_with_invalid_token(test_client, setup_db):
    response = test_client.post(
        f"/projects/3fa85f64-5717-4562-b3fc-2c963f66afa6/contribute",
        json={"amount": 1},
        headers={"Authorization": f"Bearer invalid_token"},
    )

    assert response.status_code == 401
    assert response.json().get("detail") == "Invalid token or expired token"


def test_contribute_with_invalid_amount(test_client, setup_db):
    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "test@tester.com", "password": "test"},
    )

    token = response.json().get("access_token")
    assert response.status_code == 200
    assert token
    assert response.json().get("token_type") == "bearer"

    response = test_client.post(
        "/projects",
        json={
            "title": "test",
            "description": "test",
            "goal_amount": 1,
            "deadline": "2026-01-01T12:00:00.000Z",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    id = response.json().get("id")
    assert response.status_code == 200
    assert response.json().get("title") == "test"
    assert response.json().get("description") == "test"
    assert response.json().get("goal_amount") == "1"
    assert id
    assert response.json().get("deadline")
    assert response.json().get("created_at")

    response = test_client.post(
        f"/projects/{id}/contribute",
        json={"amount": "invalid_amount"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422
    assert "Input should be a valid decimal" in response.json().get("detail")[0].get(
        "msg"
    )


def test_contribute_with_amount_not_greater_than_zero(test_client, setup_db):
    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "test@tester.com", "password": "test"},
    )

    token = response.json().get("access_token")
    assert response.status_code == 200
    assert token
    assert response.json().get("token_type") == "bearer"

    response = test_client.post(
        "/projects",
        json={
            "title": "test",
            "description": "test",
            "goal_amount": 1,
            "deadline": "2026-01-01T12:00:00.000Z",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    id = response.json().get("id")
    assert response.status_code == 200
    assert response.json().get("title") == "test"
    assert response.json().get("description") == "test"
    assert response.json().get("goal_amount") == "1"
    assert id
    assert response.json().get("deadline")
    assert response.json().get("created_at")

    response = test_client.post(
        f"/projects/{id}/contribute",
        json={"amount": 0},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422
    assert "Input should be greater than 0" in response.json().get("detail")[0].get(
        "msg"
    )


def test_contribute_with_invalid_project_id(test_client, setup_db):
    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "test@tester.com", "password": "test"},
    )

    token = response.json().get("access_token")
    assert response.status_code == 200
    assert token
    assert response.json().get("token_type") == "bearer"

    response = test_client.post(
        f"/projects/invalid_id/contribute",
        json={"amount": 0},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422
    assert "Input should be a valid UUID" in response.json().get("detail")[0].get("msg")


def test_contribute_with_nonexisting_project(test_client, setup_db):
    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "test@tester.com", "password": "test"},
    )

    token = response.json().get("access_token")
    assert response.status_code == 200
    assert token
    assert response.json().get("token_type") == "bearer"

    response = test_client.post(
        f"/projects/3fa85f64-5717-4562-b3fc-2c963f66afa6/contribute",
        json={"amount": 1},
        headers={"Authorization": f"Bearer {token}"},
    )

    print(response.json())

    assert response.status_code == 404
    assert response.json().get("detail") == "Project not found"


def test_contribute_with_missing_input(test_client, setup_db):
    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "test@tester.com", "password": "test"},
    )

    token = response.json().get("access_token")
    assert response.status_code == 200
    assert token
    assert response.json().get("token_type") == "bearer"

    response = test_client.post(
        "/projects",
        json={
            "title": "test",
            "description": "test",
            "goal_amount": 1,
            "deadline": "2026-01-01T12:00:00.000Z",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    id = response.json().get("id")
    assert response.status_code == 200
    assert response.json().get("title") == "test"
    assert response.json().get("description") == "test"
    assert response.json().get("goal_amount") == "1"
    assert id
    assert response.json().get("deadline")
    assert response.json().get("created_at")

    response = test_client.post(
        f"/projects/{id}/contribute", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422
    assert "Field required" in response.json().get("detail")[0].get("msg")
