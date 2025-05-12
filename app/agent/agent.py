"""
LangGraph Functional API 기반 OpenAI + Calendar MCP 연동 에이전트
"""

import os
import asyncio
from typing import Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent


def get_openai_client() -> ChatOpenAI:
    """Load OpenAI API key from environment and return a ChatOpenAI client.

    Returns:
        ChatOpenAI: An instance of the OpenAI chat client.

    Raises:
        RuntimeError: If OPENAI_API_KEY is not set in the environment.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set in the environment.")
    return ChatOpenAI(model="gpt-4o", api_key=api_key)


async def ask_agent(messages: list[dict]):
    """Main entrypoint for the LangGraph OpenAI + Calendar MCP agent demo."""

    user_message = messages[-1]["content"]

    async with MultiServerMCPClient(
        {
            "google-calendar": {
                "command": "node",
                "args": ["/Users/sewookkim/Projects/google-calendar-mcp/build/index.js"],
                "transport": "stdio",
            }
        }
    ) as client:
        openai_client = get_openai_client()
        agent = create_react_agent(
            openai_client,
            client.get_tools()
        )
        calendar_response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": user_message}]}
        )
        # print(calendar_response)
    return calendar_response


if __name__ == "__main__":

    messages = [{"role": "user", "content": "이번 주 내 일정 알려줘"}]
    response = asyncio.run(
        ask_agent(messages)
    )
    print(response)

