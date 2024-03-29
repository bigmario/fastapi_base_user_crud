from app.tests.db_mock import test_db, test_client, create_token

client = test_client

user = {
    "email": "testuser@mail.com",
    "name": "testName",
    "last_name": "testLastname",
    "phone": "testPhone",
    "password": "testPassword",
}


def test_home(test_db):
    """
    Assert home endopoint
    """
    response = client.get("/", headers={"Accept": "application/json"})
    assert response.status_code == 200
    assert response.json() == {
        "Framework": "FastAPI",
        "Message": "Base Users CRUD !!",
    }


def test_create_user(test_db):
    # When
    response = client.post(
        "/users/", json=user, headers={"Authorization": "Bearer " + create_token(user)}
    )

    # Then
    assert response.status_code == 201
    assert response.json()["email"] == user["email"]


def test_read_user(test_db):
    # Given
    response = client.post(
        "/users/", json=user, headers={"Authorization": "Bearer " + create_token(user)}
    )
    user_id = response.json()["id"]

    # When
    response = client.get(f"/users/{user_id}")

    # Then
    assert response.status_code == 200
    assert response.json()["email"] == user["email"]


def test_update_user(test_db):
    # Given
    response = client.post(
        "/users/", json=user, headers={"Authorization": "Bearer " + create_token(user)}
    )
    user_id = response.json()["id"]
    update_user = {"email": "updateduser_mail@mail.com"}

    # When
    response = client.patch(
        f"/users/{user_id}",
        json=update_user,
        headers={"Authorization": "Bearer " + create_token(user)},
    )

    # Then
    assert response.status_code == 200
    assert response.json()["email"] == update_user["email"]


def test_delete_user(test_db):
    # Given
    response = client.post(
        "/users/", json=user, headers={"Authorization": "Bearer " + create_token(user)}
    )
    user_id = response.json()["id"]

    # When
    response = client.delete(
        f"/users/{user_id}", headers={"Authorization": "Bearer " + create_token(user)}
    )

    # Then
    assert response.status_code == 200

    # Then

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 404
