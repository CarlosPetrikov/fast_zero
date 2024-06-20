from http import HTTPStatus

from jwt import decode

from fast_zero.security import SECRET_KEY, create_access_token


def test_jwt():
    data = {"test": "test"}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=["HS256"])

    assert decoded["test"] == data["test"]
    assert decoded["exp"]  # Testa se o valor de exp foi adicionado ao token


def test_invalid_username_jwt(client):
    token = create_access_token({"sub": "user_ficticio@teste.com.br"})

    response = client.delete("/users/1", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_non_existent_sub_key_jwt(client):
    token = create_access_token({})

    response = client.delete("/users/1", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_jwt_invalid_token(client):
    response = client.delete("/users/1", headers={"Authorization": "Bearer token-invalido"})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}
