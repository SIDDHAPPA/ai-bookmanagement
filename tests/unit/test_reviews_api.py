import pytest
from unittest.mock import patch

@pytest.mark.asyncio
@patch("app.services.storage.upload_file")
async def test_add_and_get_reviews(mock_upload, client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    book = await client.post(
        "/books",
        headers=headers,
        files={"file": ("book.txt", b"text", "text/plain")},
        data={
            "title": "ML Book",
            "author": "Author",
            "genre": "AI",
            "year_published": "2024"
        }
    )

    book_id = book.json()["id"]

    response = await client.post(
        f"/books/{book_id}/reviews",
        headers=headers,
        json={"review_text": "Excellent", "rating": 4.5}
    )

    assert response.status_code == 200

    response = await client.get(f"/books/{book_id}/reviews")
    assert len(response.json()) == 1
