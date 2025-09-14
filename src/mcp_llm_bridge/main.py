# src/mcp_llm_bridge/main.py
import asyncio
import argparse
from dotenv import load_dotenv
from mcp_llm_bridge.config import BridgeConfig
from mcp_llm_bridge.bridge import BridgeManager
import colorlog
import logging

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

async def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run MCP-LLM bridge")
    parser.add_argument(
        "--params",
        default="params.json",
        help="Path to JSON parameter file",
    )
    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    # Load configuration from parameter file
    config = BridgeConfig.from_file(args.params)

    logger.info(f"Starting bridge with model: {config.llm_config.model}")
    
    # Use bridge with context manager
    async with BridgeManager(config) as bridge:
        while True:
            try:
                user_input = input("\nEnter your prompt (or 'quit' to exit): ")
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                    
                response = await bridge.process_message(user_input)
                print(f"\nResponse: {response}")
                
            except KeyboardInterrupt:
                logger.info("\nExiting...")
                break
            except Exception as e:
                logger.error(f"\nError occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
