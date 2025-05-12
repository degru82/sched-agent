"""FastMCP 서버 진입점.

이 모듈은 FastMCP를 사용하여 MCP 서버를 설정하고 실행합니다.
"""
import os

from typing import Any, Dict, List
from dotenv import load_dotenv
from tavily import TavilyClient
from fastmcp import FastMCP


# Load environment variables
load_dotenv()

# Initialize Tavily client
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# FastMCP 서버 인스턴스 생성
mcp = FastMCP("LangGraph and FastMCP Official Document Search Server")


@mcp.tool()
def search_langgraph_docs(query: str) -> List[Dict[str, Any]]:
    """LangGraph 공식 문서와 GitHub 저장소를 검색합니다.

    Args:
        query: 검색할 쿼리 문자열

    Returns:
        검색 결과 목록
    """
    search_query = f"site:langchain-ai.github.io/langgraph OR site:github.com/langchain-ai/langgraph {query}"
    response = tavily_client.search(
        query=search_query,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True
    )
    return response.get("results", [])


@mcp.tool()
def search_fastmcp_docs(query: str) -> List[Dict[str, Any]]:
    """FastMCP 공식 문서와 GitHub 저장소를 검색합니다.

    Args:
        query: 검색할 쿼리 문자열

    Returns:
        검색 결과 목록
    """
    search_query = f"site:modelcontextprotocol.io OR site:github.com/modelcontextprotocol/python-sdk {query}"
    response = tavily_client.search(
        query=search_query,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True
    )
    return response.get("results", [])


if __name__ == "__main__":
    # mcp.run(transport="sse", host="0.0.0.0", port=8000) 
    mcp.run(transport="stdio")
