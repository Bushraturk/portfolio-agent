


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json
import traceback
import logging
from fastapi.middleware.cors import CORSMiddleware
from agentsapp import portfolio_agent, Runner
from connect import portfolio_input_checker, portfolio_response_checker
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# Attach guardrails to the existing agent instance
base_agent = portfolio_agent
base_agent.input_guardrails.append(portfolio_input_checker)
base_agent.output_guardrails.append(portfolio_response_checker)

# router = APIRouter(prefix="/ask_agent")

# Simple root route for healthcheck
@app.get("/Chat")
async def chat_healthcheck():
    return {"status": "ok"}

@app.post("/Chat")
async def Chat(request: Request):
    # Read raw body first so empty bodies don't cause a JSONDecodeError
    body_bytes = await request.body()
    if not body_bytes:
        data = {}
    else:
        try:
            data = json.loads(body_bytes)
        except Exception:
            return JSONResponse(status_code=400, content={"error": "Invalid JSON body"})

    message = data.get("message", "")

    try:
        result = await Runner.run(base_agent, [{"role": "user", "content": message}])
    except Exception as e:
        tb = traceback.format_exc()
        logging.exception("Error running agent")
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": tb})
    # Prefer a concise final reply. Many RunResult objects expose `final_output`.
    final_text = None
    # If the RunResult has a `final_output` attribute, use it.
    if hasattr(result, "final_output"):
        final_output = result.final_output
        if isinstance(final_output, dict):
            final_text = final_output.get("text") or str(final_output)
        else:
            final_text = str(final_output)
    else:
        # Fallback: try to extract the common nested output path
        try:
            final_text = result.output[0].content[0].get("text")
        except Exception:
            final_text = str(result)

    # Return a single clean string (no token/debug info)
    return JSONResponse(status_code=200, content={"reply": final_text})


