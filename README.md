# Sched-Agent: FastMCP + LangGraph 기반 LLM Agent 서버

## 프로젝트 개요

**Sched-Agent**는 [FastMCP](https://gofastmcp.com/)를 기반으로 Model Context Protocol(MCP) 서버를 구축하고, [LangGraph](https://langchain-ai.github.io/langgraph/) 및 [LangChain](https://python.langchain.com/)을 활용해 강력한 LLM 에이전트 기능을 제공합니다. 이 프로젝트는 Python 3.12+ 환경에서 동작하며, uv, ruff, pytest 등 최신 Python 생태계 도구를 적극 활용합니다.

---

## 주요 기술 스택

- **Python** 3.12+
- **FastMCP**: MCP 서버/클라이언트 프레임워크
- **LangGraph**: 그래프 기반 LLM 에이전트 설계
- **LangChain**: LLM 에이전트 프레임워크
- **uv**: 빠른 패키지/환경 관리
- **ruff**: 코드 포매팅/린팅
- **pytest**: 테스트
- **mlflow**: 실험 추적 (옵션)
- **streamlit**: 데모 UI (옵션)

---

## 프로젝트 구조

```
sched-agent/
├── app/
│   ├── __init__.py
│   ├── mcp_server.py         # FastMCP 서버 진입점
│   ├── agent/                # LangGraph/Agent 관련 코드
│   ├── prompts/              # 프롬프트 템플릿 및 버전 관리
│   ├── config/               # 설정 및 YAML 파일
│   └── utils/                # 유틸리티 함수
├── tests/                    # pytest 기반 테스트
├── requirements.txt
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 설치 및 실행

### 1. 의존성 설치

```bash
uv pip install -r requirements.txt
```

### 2. 서버 실행

```bash
python app/mcp_server.py
# 또는
fastmcp run app/mcp_server.py:mcp --transport sse --port 8000
```

### 3. 코드 포매팅/린팅

```bash
ruff check .
ruff format .
```

### 4. 테스트

```bash
pytest
```

---

## 예제 코드

### FastMCP 서버 (app/mcp_server.py)

```python
from fastmcp import FastMCP

mcp = FastMCP("Sched-Agent MCP Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """두 수를 더합니다."""
    return a + b

if __name__ == "__main__":
    mcp.run(transport="sse", host="127.0.0.1", port=8000)
```

### LangGraph Agent (app/agent/agent.py)

```python
from langgraph import Graph, Node
from langchain.llms import OpenAI

def build_agent() -> Graph:
    """LangGraph 기반 에이전트 그래프 생성."""
    llm = OpenAI(model="gpt-3.5-turbo")
    node = Node(llm)
    graph = Graph()
    graph.add_node("llm", node)
    return graph
```

---

## 라이선스

이 프로젝트는 Apache-2.0 라이선스를 따릅니다. 자세한 내용은 [LICENSE](./LICENSE) 파일을 참고하세요.

---

## 참고 자료

- [FastMCP 공식 문서](https://gofastmcp.com/)
- [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/)
- [LangChain 공식 문서](https://python.langchain.com/)
- [uv 공식 문서](https://github.com/astral-sh/uv)
- [ruff 공식 문서](https://docs.astral.sh/ruff/)
- [pytest 공식 문서](https://docs.pytest.org/)

---

## 기여

이 프로젝트는 오픈소스입니다. 버그 리포트, 기능 제안, PR 모두 환영합니다! 