# 🤖 Personal AI Assistant

A modular AI Assistant built with **LangGraph**, **Streamlit**, and **OpenRouter**. It supports multi-turn conversations, tool calling, and persistent chat history using SQLite.

## ✨ Features

- 💬 Interactive chat interface built with Streamlit
- 🧠 LangGraph-based conversational workflow
- 🔄 Persistent conversation memory using SQLite
- 🛠️ Tool calling support
  - Calculator
  - Web Search
  - Stock Price Lookup
- 🤖 OpenRouter LLM integration
- ⚙️ Modular and scalable project structure
- 🔐 Environment variable management using `.env`

---

## 📂 Project Structure

```
personal-ai-assistant/
│
├── app.py                 # Streamlit frontend
├── backend.py             # LangGraph workflow
│
├── config/
│   ├── __init__.py
│   ├── llm.py
│   └── settings.py
│
├── graph/
│   ├── builder.py
│   ├── nodes.py
│   └── state.py
│
├── prompts/
│   └── system_prompt.py
│
├── tools/
│   ├── calculator.py
│   ├── search.py
│   └── stocks.py
│
├── ui/
│   ├── session.py
│   └── sidebar.py
│
├── utils/
│   └── formatter.py
│
├── database/
│
└── .gitignore
```

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangGraph
- LangChain
- OpenRouter
- SQLite

## 🧠 Current Capabilities

- Natural language conversations
- Multi-turn chat
- Persistent chat sessions
- Tool calling
- Calculator
- Search
- Stock Price Lookup

---

## 🚧 Roadmap

- [ ] Persistent user memory
- [ ] PDF RAG support
- [ ] Vector Database
- [ ] Multi-Agent workflow
- [ ] Gmail & Calendar integration
- [ ] Weather integration
- [ ] Streaming responses
- [ ] Docker deployment
