import pytest
from unittest.mock import AsyncMock, patch
from mcp_llm_bridge.mcp_client import MCPClient


@pytest.mark.asyncio
async def test_sse_connection_used_with_headers():
    mock_ctx = AsyncMock()
    mock_ctx.__aenter__.return_value = ("r", "w")
    session_ctx = AsyncMock()
    session_obj = AsyncMock()
    session_ctx.__aenter__.return_value = session_obj
    session_obj.initialize = AsyncMock()

    headers = {"Authorization": "Bearer test-key"}
    with patch("mcp_llm_bridge.mcp_client.sse_client", return_value=mock_ctx) as sse_mock, \
         patch("mcp_llm_bridge.mcp_client.ClientSession", return_value=session_ctx):
        client = MCPClient(sse_url="http://example.com/sse", sse_headers=headers)
        await client.connect()
        sse_mock.assert_called_once_with("http://example.com/sse", headers=headers)
        session_obj.initialize.assert_awaited()
        assert client.session is session_obj
