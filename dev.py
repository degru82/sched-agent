"""LangGraph development server for the agent.

This module provides a development server for the agent using langgraph dev.
"""
from app.agent.agent import Agent

# Create the agent instance
agent = Agent()

# Export the graph for langgraph dev
graph = agent.graph 