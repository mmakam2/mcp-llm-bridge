# src/mcp_llm_bridge/mcp_client.py
import logging
from typing import Any, List, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s%(reset)s:     %(cyan)s%(name)s%(reset)s - %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
))

logger = colorlog.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class MCPClient:
    """Client for interacting with MCP servers"""

    def __init__(
        self,
        server_params: Optional[StdioServerParameters] = None,
        sse_url: Optional[str] = None,
        sse_headers: Optional[dict[str, str]] = None,
    ):
        if not server_params and not sse_url:
            raise ValueError("Either stdio server params or an SSE URL must be provided")

        self.server_params = server_params
        self.sse_url = sse_url
        self.sse_headers = sse_headers
        self.session = None
        self._client = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.__aexit__(exc_type, exc_val, exc_tb)
        if self._client:
            await self._client.__aexit__(exc_type, exc_val, exc_tb)

    async def connect(self):
        """Establishes connection to MCP server"""
        logger.debug("Connecting to MCP server...")

        if self.sse_url:
            logger.debug(f"Using SSE transport to {self.sse_url}")
            self._client = sse_client(self.sse_url, headers=self.sse_headers)
        else:
            logger.debug("Using stdio transport")
            self._client = stdio_client(self.server_params)
        self.read, self.write = await self._client.__aenter__()
        session = ClientSession(self.read, self.write)
        self.session = await session.__aenter__()
        await self.session.initialize()
        logger.debug("Connected to MCP server successfully")

    async def get_available_tools(self) -> List[Any]:
        """List available tools"""
        if not self.session:
            raise RuntimeError("Not connected to MCP server")
            
        logger.debug("Requesting available tools from MCP server")
        tools = await self.session.list_tools()
        logger.debug(f"Received tools from MCP server: {tools}")
        return tools

    async def call_tool(self, tool_name: str, arguments: dict) -> Any:
        """Call a tool with given arguments"""
        if not self.session:
            raise RuntimeError("Not connected to MCP server")
            
        logger.debug(f"Calling MCP tool '{tool_name}' with arguments: {arguments}")
        result = await self.session.call_tool(tool_name, arguments=arguments)
        logger.debug(f"Tool result: {result}")
        return result
