from app.auth import create_access_token, get_current_user
from fastapi import HTTPException
import pytest

def test_create_and_decode_jwt():
    token = create_access_token({"user_id": 1, "username": "alice"})
    payload = get_current_user(token)

    assert payload["user_id"] == 1
    assert payload["username"] == "alice"

def test_invalid_jwt():
    with pytest.raises(HTTPException):
        get_current_user("invalid.token.value")
