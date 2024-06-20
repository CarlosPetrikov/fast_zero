from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_get_token(client, user):
    response = client.post(
        "/token",
        data={"username": user.email, "password": user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "token_type" in token


def test_get_token_with_invalid_user(client, user):
    response = client.post(
        "/token",
        data={"username": "usuario_inexistente", "password": "senha_inexistente"},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_token_with_invalid_password(client, user):
    response = client.post(
        "/token",
        data={"username": user.email, "password": "senha_inexistente"},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_root_deve_retornar_ok_e_ola_mundo(client):
    # client = TestClient(app)  # Arrange

    response = client.get("/")  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {"message": "Olá Mundo!"}  # Assert


def test_create_user(client):
    # client = TestClient(app)

    response = client.post(
        "/users/",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secret",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "alice",
        "email": "alice@example.com",
        "id": 1,
    }


def test_create_with_existent_username(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.post(
        "/users/",
        json={
            "username": user_schema["username"],
            "email": user_schema["email"],
            "password": "senha_teste_123",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Username already exists"


def test_create_with_existent_email(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.post(
        "/users/",
        json={
            "username": "teste_user_x",
            "email": user_schema["email"],
            "password": "senha_teste_123",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Email already exists"


def test_read_users(client):
    response = client.get("/users")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users/")
    assert response.json() == {"users": [user_schema]}


def test_read_user(client):
    response = client.get("/users/1")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "User not found"


def test_read_user_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_update_user(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": user.id,
    }


def test_update_wrong_user_id(client, user, token):
    response = client.put(
        f"/users/{user.id + 1}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


# TESTE PRÉ TOKEN JWT
# def test_update_non_existent_user(client):
#     response = client.put(
#         "/users/2",
#         json={
#             "username": "bob",
#             "email": "bob@example.com",
#             "password": "mynewpassword",
#         },
#     )
#     assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client, user, token):
    response = client.delete(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_delete_wrong_user_id(client, user, token):
    response = client.delete(f"/users/{user.id + 1}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.BAD_REQUEST


# TESTE PRÉ TOKEN JWT
# def test_delete_non_existent_user(client):
#     response = client.delete("/users/1")

#     assert response.status_code == HTTPStatus.NOT_FOUND
