from mcp_llm_bridge.config import BridgeConfig


def test_from_file_allows_unescaped_newlines(tmp_path):
    params = """{"llm_config": {"api_key": "k", "model": "m"}, "system_prompt": "Line1
Line2"}"""
    path = tmp_path / "params.json"
    path.write_text(params)
    cfg = BridgeConfig.from_file(str(path))
    assert cfg.system_prompt == "Line1\nLine2"


def test_from_file_handles_comments_and_trailing_commas(tmp_path):
    params = """
    {
      // comment before object
      "llm_config": {"api_key": "k", "model": "m",},
      "system_prompt": "hi", // comment after value
    }
    """
    path = tmp_path / "params.json"
    path.write_text(params)
    cfg = BridgeConfig.from_file(str(path))
    assert cfg.llm_config.model == "m"
    assert cfg.system_prompt == "hi"
