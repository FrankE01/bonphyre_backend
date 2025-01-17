from tests.conftest import setup_db, test_client


def test_create_project(test_client, setup_db):
    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "test@tester.com", "password": "test"},
    )

    assert response.status_code == 200
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"

    response = test_client.post(
        "/projects",
        json={
            "title": "test",
            "description": "test",
            "goal_amount": 1,
            "deadline": "2026-01-01T12:00:00.000Z",
        },
        headers={"Authorization": f"Bearer {response.json().get('access_token')}"},
    )

    assert response.status_code == 200
    assert response.json().get("title") == "test"
    assert response.json().get("description") == "test"
    assert response.json().get("goal_amount") == "1"
    assert response.json().get("id")
    assert response.json().get("deadline")
    assert response.json().get("created_at")


def test_create_project_unauthenticated(test_client, setup_db):

    response = test_client.post(
        "/projects",
        json={
            "title": "test",
            "description": "test",
            "goal_amount": 1,
            "deadline": "2026-01-01T12:00:00.000Z",
        },
    )

    assert response.status_code == 401
    assert response.json().get("detail") == "Not authenticated"


def test_create_project_with_invalid_token(test_client, setup_db):

    response = test_client.post(
        "/projects",
        json={
            "title": "test",
            "description": "test",
            "goal_amount": 1,
            "deadline": "2026-01-01T12:00:00.000Z",
        },
        headers={"Authorization": f"Bearer invalid_token"},
    )

    assert response.status_code == 401
    assert response.json().get("detail") == "Invalid token or expired token"


def test_create_project_with_existing_title(test_client, setup_db):
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

    assert response.status_code == 200
    assert response.json().get("title") == "test"
    assert response.json().get("description") == "test"
    assert response.json().get("goal_amount") == "1"
    assert response.json().get("id")
    assert response.json().get("deadline")
    assert response.json().get("created_at")

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

    assert response.status_code == 400
    assert (
        response.json().get("detail")
        == "Invalid input. Make sure the title and description are unique"
    )


def test_create_project_with_invalid_goal_amount(test_client, setup_db):
    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "test@tester.com", "password": "test"},
    )

    assert response.status_code == 200
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"

    response = test_client.post(
        "/projects",
        json={
            "title": "test",
            "description": "test",
            "goal_amount": "invalid_goal_amount",
            "deadline": "2026-01-01T12:00:00.000Z",
        },
        headers={"Authorization": f"Bearer {response.json().get('access_token')}"},
    )

    assert response.status_code == 422
    assert "Input should be a valid decimal" in response.json().get("detail")[0].get(
        "msg"
    )


def test_create_project_with_goal_amount_not_greater_than_zero(test_client, setup_db):
    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "test@tester.com", "password": "test"},
    )

    assert response.status_code == 200
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"

    response = test_client.post(
        "/projects",
        json={
            "title": "test",
            "description": "test",
            "goal_amount": 0,
            "deadline": "2026-01-01T12:00:00.000Z",
        },
        headers={"Authorization": f"Bearer {response.json().get('access_token')}"},
    )

    assert response.status_code == 422
    assert "Input should be greater than 0" in response.json().get("detail")[0].get(
        "msg"
    )


def test_create_project_with_timezone_naive_deadline(test_client, setup_db):
    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "test@tester.com", "password": "test"},
    )

    assert response.status_code == 200
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"

    response = test_client.post(
        "/projects",
        json={
            "title": "test",
            "description": "test",
            "goal_amount": 1,
            "deadline": "2026-01-01T12:00:00.000",
        },
        headers={"Authorization": f"Bearer {response.json().get('access_token')}"},
    )

    assert response.status_code == 422
    assert "Deadline must have timezone info" in response.json().get("detail")[0].get(
        "msg"
    )


def test_create_project_with_past_deadline(test_client, setup_db):
    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "test@tester.com", "password": "test"},
    )

    assert response.status_code == 200
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"

    response = test_client.post(
        "/projects",
        json={
            "title": "test",
            "description": "test",
            "goal_amount": 1,
            "deadline": "2024-01-01T12:00:00.000Z",
        },
        headers={"Authorization": f"Bearer {response.json().get('access_token')}"},
    )

    assert response.status_code == 422
    assert "Deadline must be in the future" in response.json().get("detail")[0].get(
        "msg"
    )


def test_create_project_with_invalid_input_or_missing_input(test_client, setup_db):
    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "test@tester.com", "password": "test"},
    )

    assert response.status_code == 200
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"

    response = test_client.post(
        "/projects",
        json={"title": 98, "goal_amount": 1, "deadline": "2026-01-01T12:00:00.000Z"},
        headers={"Authorization": f"Bearer {response.json().get('access_token')}"},
    )

    assert response.status_code == 422


def test_get_projects(test_client, setup_db):
    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "test@tester.com", "password": "test"},
    )

    assert response.status_code == 200
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"

    response = test_client.post(
        "/projects",
        json={
            "title": "test",
            "description": "test",
            "goal_amount": 1,
            "deadline": "2026-01-01T12:00:00.000Z",
        },
        headers={"Authorization": f"Bearer {response.json().get('access_token')}"},
    )

    assert response.status_code == 200
    assert response.json().get("title") == "test"
    assert response.json().get("description") == "test"
    assert response.json().get("goal_amount") == "1"
    assert response.json().get("id")
    assert response.json().get("deadline")
    assert response.json().get("created_at")

    response = test_client.get("/projects")

    print(response.json())

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_projects_empty(test_client, setup_db):

    response = test_client.get("/projects")

    assert response.status_code == 200
    assert response.json() == []


def test_get_project(test_client, setup_db):
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

    response = test_client.get(f"/projects/{id}")

    assert response.status_code == 200
    assert response.json().get("title") == "test"
    assert response.json().get("description") == "test"
    assert response.json().get("goal_amount") == "1"
    assert response.json().get("id") == id
    assert response.json().get("deadline")
    assert response.json().get("created_at")


def test_get_nonexisting_project(test_client, setup_db):

    response = test_client.get(f"/projects/3fa85f64-5717-4562-b3fc-2c963f66afa6")

    print(response.json())

    assert response.status_code == 404
    assert response.json().get("detail") == "Project not found"


def test_get_project_with_invalid_id(test_client, setup_db):

    response = test_client.get(f"/projects/invalid_id")

    print(response.json())

    assert response.status_code == 422
    assert "Input should be a valid UUID" in response.json().get("detail")[0].get("msg")
