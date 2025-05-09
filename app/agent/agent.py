"""LangGraph 기반 에이전트 구현.

이 모듈은 LangGraph를 사용하여 LLM 에이전트를 구현합니다.
"""
from typing import Any, Dict, List, TypedDict, Annotated, Sequence
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from fastmcp import MCPClient

# Load environment variables
load_dotenv()

class AgentState(TypedDict):
    """에이전트의 상태를 나타내는 타입."""
    messages: Annotated[Sequence[HumanMessage | AIMessage], "대화 메시지"]
    next: Annotated[str, "다음 단계"]

class Agent:
    """LangGraph 기반 LLM 에이전트."""

    def __init__(self, model_name: str = "gpt-3.5-turbo") -> None:
        """에이전트 초기화.

        Args:
            model_name: 사용할 LLM 모델 이름
        """
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize MCP client
        self.mcp_client = MCPClient("http://localhost:8000")
        self.tools = self._get_mcp_tools()
        self.tool_executor = ToolExecutor(self.tools)
        
        # Build the graph
        self.graph = self._build_graph()

    def _get_mcp_tools(self) -> List[BaseTool]:
        """MCP 서버에서 사용 가능한 도구들을 가져옵니다.

        Returns:
            MCP 도구 리스트
        """
        try:
            return self.mcp_client.get_tools()
        except Exception as e:
            print(f"Warning: Failed to get MCP tools: {e}")
            return []

    def _create_agent_prompt(self) -> ChatPromptTemplate:
        """에이전트 프롬프트를 생성합니다.

        Returns:
            생성된 프롬프트 템플릿
        """
        return ChatPromptTemplate.from_messages([
            ("system", """You are a helpful AI assistant that can use tools to answer questions.
            Follow these steps:
            1. Think about what you need to do
            2. Use tools if necessary
            3. Provide a clear and concise answer
            
            Available tools: {tools}
            
            Always think step by step and explain your reasoning."""),
            MessagesPlaceholder(variable_name="messages"),
        ])

    def _build_graph(self) -> StateGraph:
        """에이전트 그래프를 구축합니다.

        Returns:
            구성된 LangGraph 그래프
        """
        # Create the graph
        workflow = StateGraph(AgentState)

        # Define the nodes
        def agent_node(state: AgentState) -> AgentState:
            """에이전트 노드: LLM을 사용하여 응답을 생성합니다."""
            messages = state["messages"]
            prompt = self._create_agent_prompt()
            
            # Generate response
            response = self.llm.invoke(
                prompt.format_messages(
                    messages=messages,
                    tools=self.tools
                )
            )
            
            # Update state
            return {
                "messages": messages + [response],
                "next": "end"
            }

        # Add nodes to the graph
        workflow.add_node("agent", agent_node)
        
        # Set the entry point
        workflow.set_entry_point("agent")
        
        # Add edges
        workflow.add_edge("agent", END)
        
        # Compile the graph
        return workflow.compile()

    async def process(self, input_text: str) -> Dict[str, Any]:
        """입력 텍스트를 처리합니다.

        Args:
            input_text: 처리할 입력 텍스트

        Returns:
            처리 결과를 담은 딕셔너리
        """
        # Initialize state
        initial_state = {
            "messages": [HumanMessage(content=input_text)],
            "next": "agent"
        }
        
        # Run the graph
        result = await self.graph.ainvoke(initial_state)
        
        # Extract the final response
        final_message = result["messages"][-1]
        
        return {
            "input": input_text,
            "output": final_message.content,
            "status": "success"
        } 