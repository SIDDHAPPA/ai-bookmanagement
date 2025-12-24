import pytest
from unittest.mock import patch

@pytest.mark.asyncio
@patch("app.services.storage.upload_file")
async def test_create_get_delete_book(mock_upload, client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = await client.post(
        "/books",
        headers=headers,
        files={
            "file": ("book.txt", b"Book content", "text/plain")
        },
        data={
            "title": "AI Book",
            "author": "OpenAI",
            "genre": "Tech",
            "year_published": "2025"
        }
    )

    assert response.status_code == 200
    book_id = response.json()["id"]

    response = await client.get(f"/books/{book_id}")
    assert response.status_code == 200

    response = await client.delete(f"/books/{book_id}", headers=headers)
    assert response.status_code == 200
