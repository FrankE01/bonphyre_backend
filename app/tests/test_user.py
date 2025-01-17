from tests.conftest import setup_db, test_client


def test_register_user(test_client, setup_db):
    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "test@tester.com", "password": "test"},
    )

    assert response.status_code == 200
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"


def test_register_user_with_invalid_email(test_client, setup_db):
    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "test_email", "password": "test"},
    )

    assert response.status_code == 422
    assert "String should match pattern" in response.json().get("detail")[0].get("msg")


def test_register_user_with_existing_email(test_client, setup_db):
    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "test@tester.com", "password": "test"},
    )

    assert response.status_code == 200
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"

    response = test_client.post(
        "/users/register",
        json={"username": "new_test", "email": "test@tester.com", "password": "test"},
    )

    assert response.status_code == 409
    assert (
        response.json().get("detail")
        == "Email or username already exists or Invalid input"
    )


def test_register_user_with_existing_username(test_client, setup_db):
    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "test@tester.com", "password": "test"},
    )

    assert response.status_code == 200
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"

    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "new_test@tester.com", "password": "test"},
    )

    assert response.status_code == 409
    assert (
        response.json().get("detail")
        == "Email or username already exists or Invalid input"
    )


def test_login_user(test_client, setup_db):
    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "test@tester.com", "password": "test"},
    )

    assert response.status_code == 200
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"

    response = test_client.post(
        "/users/login", json={"username": "test", "password": "test"}
    )

    assert response.status_code == 200
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"


def test_login_nonexisting_user(test_client, setup_db):
    response = test_client.post(
        "/users/login", json={"username": "test", "password": "test"}
    )

    assert response.status_code == 401
    assert response.json().get("detail") == "Invalid username or password"


def test_login_existing_user_with_wrong_password(test_client, setup_db):
    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "test@tester.com", "password": "test"},
    )

    assert response.status_code == 200
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"

    response = test_client.post(
        "/users/login", json={"username": "test", "password": "wrong_test"}
    )

    assert response.status_code == 401
    assert response.json().get("detail") == "Invalid username or password"


def test_get_current_user(test_client, setup_db):

    response = test_client.post(
        "/users/register",
        json={"username": "test", "email": "test@tester.com", "password": "test"},
    )

    assert response.status_code == 200
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"

    response = test_client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {response.json().get('access_token')}"},
    )

    assert response.status_code == 200
    assert response.json().get("username") == "test"
    assert response.json().get("email") == "test@tester.com"
    assert response.json().get("id")
    assert response.json().get("created_at")


def test_get_current_user_with_invalid_or_expired_token(test_client, setup_db):
    response = test_client.get(
        "/users/me", headers={"Authorization": "Bearer invalid_or_expired_token"}
    )

    assert response.status_code == 401
    assert response.json().get("detail") == "Invalid token or expired token"


def test_get_current_user_without_auth_token(test_client, setup_db):
    response = test_client.get("/users/me")

    assert response.status_code == 401
    assert response.json().get("detail") == "Not authenticated"
