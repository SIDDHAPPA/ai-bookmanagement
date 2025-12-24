from unittest.mock import patch, MagicMock
from app.services.storage import get_file_content

@patch("app.services.storage.s3")
def test_get_file_content_text(mock_s3):
    mock_body = MagicMock()
    mock_body.read.return_value = b"Sample book text"
    mock_s3.get_object.return_value = {"Body": mock_body}

    content = get_file_content("books/test.txt")
    assert content == "Sample book text"
