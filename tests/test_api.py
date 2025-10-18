import pytest
import os


@pytest.mark.asyncio
async def test_environment_variable():
    assert os.environ["ENVIRONMENT"] == "test"

@pytest.mark.asyncio
async def test_get_posts(client):
    """
    Test mínimo: verifica que el endpoint GET /posts responda 200.
    """
    response = await client.get("/posts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_user_and_get_details(client):
    """
    Test mínimo: crea un usuario y luego obtiene sus detalles.
    """
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
    }
    create_response = await client.post("/users/", json=user_data)
    assert create_response.status_code == 201
    created_user = create_response.json()
    assert created_user["username"] == user_data["username"]
    assert created_user["email"] == user_data["email"]

@pytest.mark.asyncio
async def test_get_nonexistent_user(client):
    """
    Test mínimo: intenta obtener un usuario que no existe.
    """
    response = await client.get("/users/99999")  
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_create_post_without_user(client):
    """
    Test mínimo: intenta crear un post con un user_id que no existe.
    """
    post_data = {
        "title": "Test Post",
        "content": "This is a test post.",
        "user_id": 99999,  
    }
    response = await client.post("/posts/", json=post_data)
    assert response.status_code == 404
    assert "User with id" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_comment_without_post(client):
    """
    Test mínimo: intenta crear un comentario para un post que no existe.
    """

    comment_data = {
        "text": "This is a test comment.",
        "user_id": 1,  
    }
    response = await client.post("/posts/99999/comments", json=comment_data)  # Post ID que no existe
    print(response.json())
    assert response.status_code == 404
    assert "Post with id" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_user_post_and_comment(client):
    """
    Test mínimo: crea un usuario, un post y un comentario asociado.
    """
    user_data = {
        "username": "commenter",
        "email": "commenter@example.com",
    }
    user_response = await client.post("/users/", json=user_data)
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]
    # Crear un nuevo post
    post_data = {
        "title": "Post for Comment",
        "content": "This post will have a comment.",
        "user_id": user_id,
    }
    post_response = await client.post("/posts/", json=post_data)
    assert post_response.status_code == 201
    post_id = post_response.json()["id"]
    comment_data = {
        "text": "This is a comment.",
        "user_id": user_id,
    }
    comment_response = await client.post(f"/posts/{post_id}/comments", json=comment_data)
    assert comment_response.status_code == 201
    created_comment = comment_response.json()
    assert created_comment["text"] == comment_data["text"]
    assert created_comment["author"]["id"] == user_id  
    print(post_response.json())