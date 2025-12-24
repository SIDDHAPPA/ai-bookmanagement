import pytest
from unittest.mock import AsyncMock, patch
from app.services.llm_client import generate_summary

@pytest.mark.asyncio
async def test_generate_summary_mocked():
    with patch(
        "app.services.llm_client.llm.ainvoke",
        AsyncMock(return_value=type("Obj", (), {"content": "Mock AI Summary"}))
    ):
        result = await generate_summary("Test content")
        assert result == "Mock AI Summary"
