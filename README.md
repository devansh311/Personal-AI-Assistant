# 🤖 Personal AI Assistant

A modular, production-grade AI assistant built with **LangGraph**, **Streamlit**, **Groq**, **PostgreSQL**, and **RAG** — capable of multi-step reasoning, real tool execution, Human-in-the-Loop confirmation flows, document-grounded answers, and full Docker deployment.

---

## 🚀 Features

### 🧠 Core AI
- Conversational AI powered by **Groq (Llama 3.1 8B)**
- Short-term conversational memory using **PostgreSQL + LangGraph checkpointer**
— conversation history persists within each thread across page refreshes
- Multi-thread conversation management — switch between chats, threads survive refresh
- Multi-step reasoning with **LangGraph state graph**
- Full **LangSmith** tracing for observability and debugging

### 🛠️ Tools
| Tool | Description |
|---|---|
| 🧮 Calculator | Solves mathematical expressions |
| 🌐 Web Search | Retrieves real-time information via DuckDuckGo |
| 📈 Stock Price | Live stock prices via Alpha Vantage |
| 🌦️ Weather | Current weather conditions via OpenWeather API |
| 📄 Document Q&A | RAG-powered answers from uploaded PDFs |
| 📅 Calendar Read | Fetches upcoming Google Calendar events via OAuth |
| ➕ Calendar Create | Creates events with **Human-in-the-Loop confirmation** |

### 📄 RAG Pipeline
- Upload PDFs via the sidebar
- Chunking with `RecursiveCharacterTextSplitter` (1000 chars, 200 overlap)
- Semantic embeddings using `BAAI/bge-small-en-v1.5` (runs locally)
- Persistent vector storage with **ChromaDB**
- Grounded answers — model says when info isn't in documents

### 🔐 Human-in-the-Loop (HITL)
- Calendar create operations use LangGraph `interrupt()`
- Graph **physically pauses** mid-execution — LLM cannot bypass confirmation
- User must type yes/no before any calendar modification executes
- Graph resumes from exact pause point after confirmation
- Supports mid-flow edits (e.g. changing event duration before confirming)

### 🗄️ Production Database
- **PostgreSQL** replaces SQLite for production-grade persistence
- Conversation history survives page refresh, server restart, and redeployment
- Multi-user ready — each thread_id is fully isolated
- Docker volume ensures data persists across container restarts

---

## 🏗️ Architecture

```
Streamlit UI → LangGraph Graph → LLM + Tools → External Services
                    ↓
            PostgresSaver (PostgreSQL)
```

### Graph Flow
```
START → chat_node → tools_condition
                        ↓ (tool called)
                    tool_node → after_tools_routing
                                    ├── prepare_calendar_event
                                    │       ↓
                                    │   calendar_confirmation_node
                                    │   (HITL interrupt — graph pauses)
                                    │       ↓ yes/no
                                    │      END
                                    └── other tools → chat_node → END
```

---

## 📂 Project Structure

```
personal-ai-assistant/
│
├── app.py                  # Streamlit entry point + HITL flow handling
├── backend.py              # Exposes compiled graph
├── Dockerfile              # Container definition for the app
├── docker-compose.yml      # App + PostgreSQL services
│
├── config/
│   ├── llm.py              # Groq LLM + LangSmith setup
│   └── settings.py         # Environment variable loader
│
├── graph/
│   ├── builder.py          # Graph nodes, edges, PostgreSQL checkpointer
│   ├── nodes.py            # chat_node, calendar_confirmation_node
│   └── state.py            # ChatState definition
│
├── prompts/
│   └── system_prompt.py    # System prompt with strict tool usage rules
│
├── rag/
│   ├── loader.py           # PDF ingestion with PyPDFLoader
│   ├── splitter.py         # RecursiveCharacterTextSplitter
│   ├── embeddings.py       # HuggingFace BAAI embeddings
│   ├── vectorstore.py      # ChromaDB persistence
│   ├── retriever.py        # Semantic search (top-k chunks)
│   └── chain.py            # Grounded QA chain
│
├── tools/
│   ├── calculator.py       # Math expressions
│   ├── search.py           # DuckDuckGo web search
│   ├── stocks.py           # Alpha Vantage stock prices
│   ├── weather.py          # OpenWeather current conditions
│   ├── calendar.py         # Google Calendar read/create + HITL + OAuth
│   └── rag.py              # ask_documents tool wrapper
│
├── ui/
│   ├── session.py          # Session init + thread persistence (JSON)
│   └── sidebar.py          # Thread selector + new chat button
│
├── utils/
│   └── formatter.py        # AIMessage content normalization
│
├── uploads/                # Runtime PDF uploads (gitignored)
├── vector_db/              # ChromaDB embeddings (gitignored)
├── database/               # Thread metadata JSON (gitignored)
├── credentials/            # Google OAuth files (gitignored)
│
├── .env.example
├── .gitignore
└── requirements.txt
```
