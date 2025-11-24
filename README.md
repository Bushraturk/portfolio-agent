# Backend (AI Agent) — README

Short guide to run and troubleshoot the backend AI agent for this project.

**Project structure (important files)**n+- `agentsapp.py`: creates the `portfolio_agent`, LLM client and tools.
- `connect.py`: guardrail functions and helper wiring used by the agent.
- `main.py`: FastAPI app exposing the `/Chat` endpoint (run with `uvicorn`).
- `pyproject.toml` / `requirments.txt`: dependency information.

**Prerequisites**
- Python 3.11 or newer.
- A virtual environment is highly recommended.
- Required packages (see `pyproject.toml`): `fastapi`, `uvicorn`, `python-dotenv`, `openai-agents` (or equivalent package that provides the `agents` module).

1) Create & activate a venv (Windows PowerShell)
```
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2) Install dependencies
```
pip install -r requirments.txt
# or install from pyproject dependencies
pip install fastapi "openai-agents>=0.3.3" python-dotenv uvicorn
```

3) Environment variables
- Create a `.env` file in the `backend` folder or set env vars in your system.
- Minimum useful variables:
  - `OPENAI_API_KEY` — (optional) used by some libraries for tracing.
  - `GEMINI_API_KEY` — the API key used by the Gemini-compatible endpoint configured in `agentsapp.py`.

Example `.env`:
```
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=ya29...
```

4) Run the app
```
# from the backend folder
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

5) Test the `/Chat` endpoint

curl example:
```
curl -X POST "http://127.0.0.1:8000/Chat" -H "Content-Type: application/json" -d '{"message":"Tell me about Bushra"}'
```

PowerShell example:
```
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/Chat -Body (ConvertTo-Json @{ message = 'Tell me about Bushra' }) -ContentType 'application/json'
```

Common issues & troubleshooting
- ModuleNotFoundError: No module named 'agents'
  - This means the package that provides `agents` (e.g. `openai-agents`) is not installed in the active environment. Activate the venv and run `pip install openai-agents` (or `pip install -r requirments.txt`).
  - If it's installed but still missing, ensure you're running `uvicorn` with the same Python environment (`python -m uvicorn main:app` is safer than a global `uvicorn` binary).

- Syntax or Import errors from `agentsapp.py`
  - `agentsapp.py` must import symbols from the `agents` package correctly. If you see syntax errors (e.g., an unfinished `from ` line), open `agentsapp.py` and fix the top-level imports so they match the installed library API.

- HTTP 500 Internal Server Error from `/Chat`
  - `main.py` now returns a JSON response including the exception and traceback when `Runner.run` fails. Check the server logs or response body to see the exact traceback and post it if you need help diagnosing it.

Notes about this repo
- `main.py` attaches two guardrail functions from `connect.py` to the `portfolio_agent` and exposes a single `POST /Chat` endpoint which returns a concise `reply` string.
- `agentsapp.py` creates the `portfolio_agent` and a small `read_portfolio_pdf` tool that returns a short portfolio summary. Ensure the referenced PDF filename exists, or the tool falls back to a default message.

If you want, I can:
- try to run the server here and capture the traceback for any 500 errors (I can’t actually run on your machine, but I can patch files). 
- fix common import issues in `agentsapp.py` so the app starts cleanly. 

Tell me which action you prefer next.
