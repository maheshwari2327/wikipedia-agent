# Wikipedia Research Assistant CLI Agent

An interactive conversational research CLI agent built with **LangChain**, **LangGraph** (`create_react_agent`), and **Ollama** (`llama3.2`), featuring a custom **Wikipedia** tool.

---

## Architecture & Stack

- **LLM**: Ollama `llama3.2` with `temperature=0.3` via `langchain-ollama`
- **Agent Loop**: LangGraph `create_react_agent` prebuilt ReAct loop with `MemorySaver` checkpointer for session conversational memory
- **Tool**: `search_wikipedia` powered by the `wikipedia` Python package (free, no API key required)

---

## File Structure

```
wikipedia agent/
├── .venv/               # Virtual environment
├── requirements.txt     # Python dependencies
├── tools.py             # search_wikipedia tool with error handling
├── agent.py             # build_agent(), ask(), and main() CLI chat loop
├── app.py               # Streamlit web application interface
└── README.md            # Documentation
```

---

## How to Run

### 1. Ensure Ollama is running
```bash
ollama run llama3.2
```

### 2. Activate Virtual Environment
On Windows:
```powershell
.venv\Scripts\activate
```

---

## Running Options

### Option A: Run in Website (Web Browser via Streamlit)
Launch the interactive web UI:
```powershell
.venv\Scripts\streamlit run app.py
```
This opens the web app automatically at `http://localhost:8501`.

### Option B: Run in Terminal (CLI Mode)
```powershell
.venv\Scripts\python agent.py
```

