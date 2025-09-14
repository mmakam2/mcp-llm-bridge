# src/mcp_llm_bridge/config.py
import json
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

    @classmethod
    def from_dict(cls, data: dict) -> "BridgeConfig":
        """Create a BridgeConfig from a dictionary."""
        llm_cfg = LLMConfig(**data["llm_config"])

        server_params = None
        if data.get("mcp_server_params"):
            server_params = StdioServerParameters(**data["mcp_server_params"])

        return cls(
            llm_config=llm_cfg,
            mcp_server_params=server_params,
            mcp_sse_url=data.get("mcp_sse_url"),
            mcp_sse_api_key=data.get("mcp_sse_api_key"),
            system_prompt=data.get("system_prompt"),
        )

    @classmethod
    def from_file(cls, path: str) -> "BridgeConfig":
        """Load configuration from a JSON file."""
        with open(path) as f:
            data = json.load(f)
        return cls.from_dict(data)
