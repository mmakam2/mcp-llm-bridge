import pytest
from types import SimpleNamespace
from mcp_llm_bridge.llm_client import LLMResponse


def test_llm_response_missing_choices():
    completion = SimpleNamespace(choices=None)
    with pytest.raises(ValueError):
        LLMResponse(completion)


def test_llm_response_empty_choices():
    completion = SimpleNamespace(choices=[])
    with pytest.raises(ValueError):
        LLMResponse(completion)
