
import pytest
from app.tests.db_mock import test_db, test_client, create_token

client = test_client

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
    # Given
    user = {
        "email": "testuser@mail.com", 
        "name": "testpassword",
        "last_name": "testpassword",
        "phone": "123456",
        "password": "12345678"
    }

    # When
    response = client.post("/users/", json=user, headers={"Authorization": "Bearer " + create_token(user)})

    # Then
    assert response.status_code == 201
    assert response.json()["email"] == user["email"]
    