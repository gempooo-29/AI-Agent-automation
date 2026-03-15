from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from rag import read_and_index_file, search_in_file
from weather import get_weather
from youtube import youtube_search
import uvicorn

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

app_graph = graph.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "user_1"}}

# ── FastAPI ────────────────────────────────────────────
app = FastAPI()

class Message(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/chat")
async def chat(msg: Message):
    response = app_graph.invoke(
        {"messages": [HumanMessage(content=msg.message)]},
        config=config
    )
    return {"response": response["messages"][-1].content}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)