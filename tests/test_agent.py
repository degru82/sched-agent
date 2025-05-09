"""에이전트 테스트 모듈."""
import pytest

from app.agent.agent import Agent

@pytest.fixture
def agent() -> Agent:
    """테스트용 에이전트 픽스처."""
    return Agent()

@pytest.mark.asyncio
async def test_agent_process(agent: Agent) -> None:
    """에이전트 처리 테스트."""
    result = await agent.process("테스트 입력")
    assert isinstance(result, dict)
    assert "input" in result
    assert "output" in result
    assert "status" in result
    assert result["status"] == "success" 