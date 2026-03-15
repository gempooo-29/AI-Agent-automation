from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from youtube import youtube_search
import os
import pyowm
from langchain_core.tools import tool
from weather import get_weather
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from rag import read_and_index_file, search_in_file

load_dotenv()

# ── Tools ──────────────────────────────────────────────
tools = [TavilySearch(max_results=3), read_and_index_file, search_in_file, get_weather, youtube_search]

# ── State ──────────────────────────────────────────────
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# ── LLM ────────────────────────────────────────────────
llm = ChatGroq(model="llama-3.3-70b-versatile").bind_tools(tools)

# ── Agent Node ─────────────────────────────────────────
def agent_node(state: AgentState):
    system = SystemMessage(content="""You are a helpful assistant with access to tools.

Rules:
- If the user is just chatting or introducing themselves → respond normally without using any tool
- If the user asks about WEATHER in any city → use get_weather tool
- If the user asks to READ a FILE → use read_and_index_file tool, then just confirm the file was read successfully. Do NOT summarize unless the user asks.
- If the user explicitly asks to SUMMARIZE → use search_in_file tool with query "main topics and summary"
- If the user asks a specific question about a file → use search_in_file tool with the user's question
- If the user asks to SEARCH or find NEWS online → use web_search tool
- If the user asks to play or find a VIDEO or SONG → use youtube_search tool                           
- NEVER use web_search for weather questions, always use get_weather tool
- NEVER use any tool for casual conversation or greetings
- NEVER mention tool names in your response
- NEVER summarize a file unless the user explicitly asks for a summary
""")
    messages = [system] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

# ── Build Graph ────────────────────────────────────────
memory = MemorySaver()

graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))

graph.set_entry_point("agent")
graph.add_conditional_edges("agent", tools_condition)
graph.add_edge("tools", "agent")

app = graph.compile(checkpointer=memory)

# ── Config ─────────────────────────────────────────────
config = {"configurable": {"thread_id": "user_1"}}

# ── Run ────────────────────────────────────────────────
print("Agent is running! Type 'exit' to quit\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    response = app.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config=config
    )

    print(f"Agent: {response['messages'][-1].content}\n")