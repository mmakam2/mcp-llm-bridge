# src/mcp_llm_bridge/config.py
from dataclasses import dataclass
from typing import Optional
from mcp import StdioServerParameters

@dataclass
class LLMConfig:
    """Configuration for LLM client"""
    api_key: str
    model: str
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000

@dataclass
class BridgeConfig:
    """Configuration for the MCP-LLM Bridge"""
    llm_config: LLMConfig
    mcp_server_params: Optional[StdioServerParameters] = None
    mcp_sse_url: Optional[str] = None
    mcp_sse_api_key: Optional[str] = None
    system_prompt: Optional[str] = None
