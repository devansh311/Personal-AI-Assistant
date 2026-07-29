# 🤖 Personal AI Assistant

A modular, production-grade AI assistant built with **LangGraph**, **Streamlit**, **Groq**, and **RAG** — capable of multi-step reasoning, real tool execution, Human-in-the-Loop confirmation flows, and document-grounded answers.

---

## 🚀 Features

### 🧠 Core AI
- Conversational AI powered by **Groq (Llama 3.1)**
- Persistent chat memory using **SQLite + LangGraph checkpointer**
- Multi-step reasoning with **LangGraph state graph**
- Full **LangSmith** tracing for observability and debugging

### 🛠️ Tools
| Tool | Description |
|---|---|
| 🧮 Calculator | Solves mathematical expressions |
| 🌐 Web Search | Retrieves real-time web information via DuckDuckGo |
| 📈 Stock Price | Fetches live stock prices via Alpha Vantage |
| 🌦️ Weather | Current weather conditions via OpenWeather API |
| 📄 Document Q&A | RAG-powered answers from your uploaded PDFs |
| 📅 Calendar Read | Fetches upcoming Google Calendar events via OAuth |
| ➕ Calendar Create | Creates events with **Human-in-the-Loop confirmation** |


### 📄 RAG Pipeline
- Upload PDFs via the sidebar
- Automatic chunking with `RecursiveCharacterTextSplitter`
- Semantic embeddings using `BAAI/bge-small-en-v1.5`
- Persistent vector storage with **ChromaDB**
- Grounded answers — model explicitly says when info isn't in documents

### 🔐 Human-in-the-Loop (HITL)
- Calendar create and delete operations **pause the graph** using LangGraph `interrupt()`
- User must explicitly confirm before any calendar modification
- Graph resumes exactly where it paused after confirmation

---

## 🏗️ Architecture

```
Streamlit UI → LangGraph Graph → LLM + Tools → External Services
                    ↓
             SqliteSaver (memory)
```

### Graph Flow
```
START → chat_node → tools_condition
                        ↓ (if tool called)
                    tool_node → after_tools_routing
                                    ↓ prepare_calendar_event
                            calendar_confirmation_node (HITL interrupt)
                                    ↓ yes/no
                                  END
                                    ↓ other tools
                              chat_node → END
```

---

## 📂 Project Structure

```
personal-ai-assistant/
│
├── app.py                  # Streamlit entry point
├── backend.py              # Exposes compiled graph
│
├── config/
│   ├── llm.py              # Groq LLM configuration + LangSmith setup
│   └── settings.py         # Environment variable loader
│
├── graph/
│   ├── builder.py          # Graph construction, edges, compilation
│   ├── nodes.py            # chat_node, calendar_confirmation_node, delete_confirmation_node
│   └── state.py            # ChatState definition
│
├── prompts/
│   └── system_prompt.py    # System prompt with tool usage rules
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
│   ├── calendar.py         # Google Calendar read/create + HITL
│   └── rag.py              # ask_documents tool wrapper
│
├── ui/
│   ├── session.py          # Streamlit session state management
│   └── sidebar.py          # Thread selector and sidebar rendering
│
├── utils/
│   └── formatter.py        # AIMessage content normalization
│
├── uploads/                # Runtime PDF uploads (gitignored)
├── vector_db/              # ChromaDB persistence (gitignored)
├── database/               # SQLite checkpoints (gitignored)
├── credentials/            # Google OAuth files (gitignored)
│
├── .env.example            # Template for environment variables
├── .gitignore
└── requirements.txt
```

---

## 🔮 Upcoming Features

- [ ] Auto-index PDFs on upload (no manual indexing)
- [ ] Source citations in RAG answers (document name + page number)
- [ ] Gmail integration (read + summarize emails)
- [ ] Long-term user memory
- [ ] Streaming responses

- [ ] Voice input support

---

## 🧑‍💻 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| UI | Streamlit |
| Agent framework | LangGraph |
| LLM framework | LangChain |
| LLM | Groq (Llama 3.1 8B) |
| Vector DB | ChromaDB |
| Embeddings | HuggingFace BAAI/bge-small-en-v1.5 |
| Conversation storage | SQLite |
| Observability | LangSmith |
| Search | DuckDuckGo |
| Calendar | Google Calendar API (OAuth) |
| Weather | OpenWeather API |
| Stocks | Alpha Vantage API |