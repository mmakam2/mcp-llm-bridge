# src/mcp_llm_bridge/config.py
import json
import re
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
        with open(path, encoding="utf-8") as f:
            raw = f.read()

        # Allow a slightly more relaxed JSON format so users can add
        # comments or trailing commas in their configuration files.  This
        # mirrors the flexibility offered by many modern config formats and
        # prevents confusing ``JSONDecodeError`` messages.
        #
        # ``strict=False`` already permits unescaped control characters
        # (e.g. newlines in strings).  Here we additionally strip
        # single-line (//) and block (/* */) comments as well as trailing
        # commas before closing brackets or braces.
        def _normalize(s: str) -> str:
            # Remove // comments
            s = re.sub(r"//.*", "", s)
            # Remove /* */ comments
            s = re.sub(r"/\*.*?\*/", "", s, flags=re.DOTALL)
            # Remove trailing commas
            s = re.sub(r",(\s*[}\]])", r"\1", s)
            return s

        raw = _normalize(raw)
        try:
            data = json.loads(raw, strict=False)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON configuration in {path}: {exc}") from exc
        return cls.from_dict(data)
