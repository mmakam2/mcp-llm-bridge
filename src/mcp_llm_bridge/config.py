# src/mcp_llm_bridge/config.py
import json
from dataclasses import dataclass
from typing import Optional
from mcp import StdioServerParameters

try:  # pragma: no cover - optional dependency
    import json5  # type: ignore
except Exception:  # pragma: no cover - narrow scope not required
    json5 = None

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
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        try:
            if json5:
                data = json5.loads(raw, strict=False)
            else:
                data = json.loads(raw, strict=False)
        except Exception as exc:  # json5 and json raise different exceptions
            raise ValueError(f"Invalid JSON configuration in {path}: {exc}") from exc
        return cls.from_dict(data)
