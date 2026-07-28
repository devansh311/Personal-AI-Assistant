# 🤖 Personal AI Assistant

A modular AI Assistant built with **LangGraph**, **Streamlit**, and **OpenRouter**, capable of reasoning, using tools, and maintaining conversation memory.

---

## 🚀 Features

- 💬 Conversational AI powered by OpenRouter
- 🧠 Persistent chat memory using SQLite
- 🔄 Multi-step reasoning with LangGraph
- 🧮 Calculator Tool
- 🌐 Web Search Tool
- 📈 Stock Price Tool
- 🌦️ Live Weather Tool
- 📊 LangSmith tracing for debugging and observability
- 🎨 Clean Streamlit chat interface
- 🔧 Modular architecture for easy feature expansion

---

## 🛠️ Tech Stack

### AI Framework
- LangGraph
- LangChain

### LLM
- OpenRouter

### Frontend
- Streamlit

### Database
- SQLite

### APIs
- OpenWeather API
- Tavily Search API
- Alpha Vantage API

### Observability
- LangSmith

---

## 📂 Project Structure

```text
personal-ai-agent/
│
├── app.py
├── backend.py
├── config/
│   ├── llm.py
│   └── settings.py
├── database/
├── graph/
│   ├── builder.py
│   ├── nodes.py
│   └── state.py
├── prompts/
│   └── system_prompt.py
├── tools/
│   ├── calculator.py
│   ├── search.py
│   ├── stocks.py
│   └── weather.py
├── ui/
├── utils/
├── requirements.txt
└── README.md
```

---
---

## 🧠 Current Toolset

| Tool | Description |
|------|-------------|
| Calculator | Solves mathematical expressions |
| Web Search | Retrieves up-to-date web information |
| Stock Price | Fetches real-time stock prices |
| Weather | Provides current weather conditions |

---

## 📊 LangSmith Tracing

LangSmith is integrated for:

- Graph execution visualization
- Tool call inspection
- LLM request & response tracing
- Latency analysis
- Error debugging
- Conversation replay

---

## 📌 Upcoming Features

- 📅 Google Calendar Integration
- 📧 Gmail Integration
- 🗺️ Maps & Places Search
- 🧠 Long-Term Memory
- 📂 Document Q&A (RAG)
- 🎤 Voice Assistant
- 🌐 Web Browser Agent
- ⚡ Streaming Responses

---