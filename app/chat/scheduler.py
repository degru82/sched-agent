"""
Streamlit chat app for scheduling with LangGraph OpenAI + Calendar MCP agent.
"""

import os
import asyncio
from typing import Any, List
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage
import logging
import traceback

# Import agent creation logic from app.agent.agent
from app.agent.agent import ask_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent


def ask_scheduler(user_messages: List[dict]) -> Any:
    """Create and return a LangGraph agent instance."""
    load_dotenv()
    return ask_agent(user_messages)


def run_agent(agent: Any, user_messages: List[dict]) -> Any:
    """Run the agent asynchronously with the given user messages."""
    return asyncio.run(agent.ainvoke({"messages": user_messages}))


def extract_last_ai_message_content(messages: list[Any]) -> str:
    """Extract the content of the last AIMessage from a list of messages.

    Args:
        messages (list[Any]): List of message objects or dicts.

    Returns:
        str: The content of the last AIMessage, or an empty string if not found.
    """
    for msg in reversed(messages):
        # Handle both dict and object cases
        if isinstance(msg, AIMessage):
            return getattr(msg, "content", "")
        if isinstance(msg, dict) and msg.get("type") == "ai":
            return msg.get("content", "")
    return ""


def main() -> None:
    """Streamlit app entrypoint for chat-based scheduling agent."""
    st.set_page_config(page_title="일정 에이전트 채팅", page_icon="📅")
    st.title("📅 일정 에이전트 채팅")
    st.markdown("Google Calendar와 연동된 AI 일정 비서에게 자연어로 일정을 요청하세요.")

    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("메시지를 입력하세요...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("에이전트가 응답 중입니다..."):
            try:
                logging.info(f"chat_history: {st.session_state.chat_history}")
                logging.info(f"chat_history type: {type(st.session_state.chat_history)}")
                response = asyncio.run(
                    ask_scheduler(
                        list(st.session_state.chat_history)
                    )
                )
                # Extract only the last AIMessage content
                ai_content = ""
                if isinstance(response, dict) and "messages" in response:
                    ai_content = extract_last_ai_message_content(response["messages"])
                if ai_content:
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_content})
                else:
                    st.session_state.chat_history.append({"role": "assistant", "content": "(AI 응답을 찾을 수 없습니다)"})
            except Exception as e:
                tb_str = traceback.format_exc()
                logging.error(f"에이전트 실행 중 오류 발생: {e}\n{tb_str}")
                st.error(f"에이전트 실행 중 오류 발생: {e}\n\nTraceback:\n{tb_str}")

    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

if __name__ == "__main__":
    main() 