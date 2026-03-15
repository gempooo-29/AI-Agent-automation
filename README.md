# 🤖 AI Agent Automation

An autonomous AI Agent built with **LangChain** + **LangGraph** that can search the web, read and summarize documents, check the weather, play YouTube videos, and hold intelligent conversations — all through a sleek Chat UI in the browser.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Web Search** | Search the internet for latest news and information |
| 📄 **File Reader** | Read and summarize PDF, DOCX, and TXT files using RAG |
| 🌤 **Weather** | Get real-time weather for any city in the world |
| 🎵 **YouTube Search** | Search and open any video or song on YouTube |
| 🧠 **Memory** | Remembers the full conversation within a session |
| 💬 **Chat UI** | Beautiful browser-based chat interface |

---

## 🏗 Architecture

Built using **LangGraph** with a ReAct-style agent loop:

```
START
  ↓
[agent_node] ← LLM decides what to do
  ↓
Tool needed?
  ├── YES → [tools_node] → back to agent
  └── NO  → END
```

The agent autonomously decides which tool to use based on your request — no hardcoded logic.

---

## 🗂 Project Structure

```
ai_agent/
├── app.py              # FastAPI server + LangGraph agent
├── rag.py              # RAG pipeline (file indexing + search)
├── weather.py          # Weather tool
├── youtube.py          # YouTube search tool
├── index.html          # Chat UI
├── requirements.txt    # Python dependencies
└── .env.example        # Environment variables template
```

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/gempooo-29/AI-Agent-automation.git
cd AI-Agent-automation
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

| Key | Where to get it |
|-----|----------------|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) — Free |
| `TAVILY_API_KEY` | [app.tavily.com](https://app.tavily.com) — Free |

> ✅ No other API keys needed — Weather uses `wttr.in` which is completely free!

---

## ▶️ Run

```bash
python app.py
```

Then open your browser at:
```
http://localhost:8000
```

---

## 💬 Example Usage

```
You: my name is Gamil
Agent: Nice to meet you, Gamil! How can I help you today?

You: what is the weather in Cairo?
Agent: Weather in Cairo: Partly Cloudy, 15°C, Humidity 67%

You: search for latest AI news
Agent: Here are the latest AI developments...

You: read the file report.pdf from C:/Users/Gamil/Downloads
Agent: File indexed successfully! You can now ask questions about it.

You: summarize it
Agent: The file discusses...

You: play Bohemian Rhapsody by Queen
Agent: Opening YouTube search for 'Bohemian Rhapsody Queen' in your browser ✅
```

---

## 🛠 Tools

### 🔍 Web Search
Uses **Tavily API** to search the internet for real-time information.

### 📄 File Reader (RAG)
Uses **LangChain + ChromaDB + HuggingFace Embeddings** to:
- Index documents into vector chunks
- Retrieve only the most relevant sections when answering questions
- Supports PDF, DOCX, and TXT files

### 🌤 Weather
Uses **wttr.in** — completely free, no API key required.

### 🎵 YouTube Search
Searches YouTube and opens the result directly in your browser.

---

## 🧠 Tech Stack

| Technology | Purpose |
|-----------|---------|
| [LangChain](https://langchain.com) | LLM framework and tools |
| [LangGraph](https://langchain-ai.github.io/langgraph) | Agent orchestration |
| [Groq](https://groq.com) | LLM inference (llama-3.3-70b) |
| [ChromaDB](https://trychroma.com) | Vector store for RAG |
| [HuggingFace](https://huggingface.co) | Embeddings model |
| [FastAPI](https://fastapi.tiangolo.com) | Backend server |
| [Tavily](https://tavily.com) | Web search API |

---

## 📄 License

MIT License — feel free to use and modify.
