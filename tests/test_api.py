import pytest
import os
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_environment_variable():
    """Verifica que el entorno de prueba esté activo."""
    # Este test no se ve afectado por los cambios en la API.
    assert os.environ.get("ENVIRONMENT") == "test"

@pytest.mark.asyncio
async def test_get_posts(client: AsyncClient):
    """Verifica que el endpoint GET /posts responda 200 OK."""
    response = await client.get("/posts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_user_and_get_details(client: AsyncClient):
    """Prueba el "happy path": crear un usuario y luego obtener sus detalles."""
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
    }
    create_response = await client.post("/users/", json=user_data)
    assert create_response.status_code == 201
    created_user = create_response.json()
    assert created_user["username"] == user_data["username"]
    assert created_user["email"] == user_data["email"]

    user_id = created_user["id"]
    get_response = await client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == user_id



@pytest.mark.asyncio
async def test_get_nonexistent_user(client: AsyncClient):
    """Verifica que intentar obtener un usuario que no existe devuelva 404."""
    user_id = 99999
    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"User with id {user_id} not found"

@pytest.mark.asyncio
async def test_create_post_with_nonexistent_user(client: AsyncClient):
    """Verifica que crear un post con un user_id inválido devuelva 422."""
    post_data = {
        "title": "Test Post",
        "content": "This is a test post.",
        "user_id": 99999,  # Este ID de usuario no existe
    }
    response = await client.post("/posts/", json=post_data)
    assert response.status_code == 422
    assert "User with id" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_user_with_duplicate_email(client: AsyncClient):
    """
    Verifica que intentar crear un usuario con un email duplicado
    devuelva 409 Conflict.
    """
    user_data = {
        "username": "duplicate_user",
        "email": "duplicate@example.com",
    }
    response1 = await client.post("/users/", json=user_data)
    assert response1.status_code == 201

    response2 = await client.post("/users/", json=user_data)
    assert response2.status_code == 409
    assert "already registered" in response2.json()["detail"]

@pytest.mark.asyncio
async def test_create_comment_for_nonexistent_post(client: AsyncClient):
    """
    Verifica que crear un comentario para un post que no existe
    devuelva 404 Not Found.
    """
    user_data = {"username": "comment_user", "email": "comment_user@example.com"}
    user_response = await client.post("/users/", json=user_data)
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]

    comment_data = {
        "text": "This is a test comment.",
        "user_id": user_id,
    }
    response = await client.post("/posts/99999/comments", json=comment_data)
    assert response.status_code == 404
    assert "Post with id" in response.json()["detail"]

@pytest.mark.asyncio
async def test_create_comment_with_nonexistent_user(client: AsyncClient):
    """
    Verifica que crear un comentario con un user_id inválido
    devuelva 422 Unprocessable Entity.
    """
    user_res = await client.post("/users/", json={"username": "post_creator", "email": "creator@example.com"})
    user_id = user_res.json()["id"]
    post_res = await client.post("/posts/", json={"title": "A post", "content": "Some content", "user_id": user_id})
    post_id = post_res.json()["id"]

    comment_data = {
        "text": "This comment has an invalid author.",
        "user_id": 99999,
    }
    response = await client.post(f"/posts/{post_id}/comments", json=comment_data)
    assert response.status_code == 422
    assert "User with id" in response.json()["detail"]

@pytest.mark.asyncio
async def test_full_flow_create_user_post_and_comment(client: AsyncClient):
    """
    Prueba el flujo completo: crear usuario, luego post, luego comentario.
    Este es un "happy path" integral.
    """
    user_data = {"username": "full_flow_user", "email": "full_flow@example.com"}
    user_response = await client.post("/users/", json=user_data)
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]

    post_data = {"title": "Full Flow Post", "content": "Content here", "user_id": user_id}
    post_response = await client.post("/posts/", json=post_data)
    assert post_response.status_code == 201
    post_id = post_response.json()["id"]

    comment_data = {"text": "A comment on the full flow post", "user_id": user_id}
    comment_response = await client.post(f"/posts/{post_id}/comments", json=comment_data)
    assert comment_response.status_code == 201
    created_comment = comment_response.json()
    assert created_comment["text"] == comment_data["text"]
    assert created_comment["author"]["id"] == user_id