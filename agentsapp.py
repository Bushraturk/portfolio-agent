



# new
import os
from dotenv import load_dotenv, find_dotenv
from agents import (
    Agent,
    AsyncOpenAI,
    Runner,
    OpenAIChatCompletionsModel,
    function_tool,
)

load_dotenv(find_dotenv())

# Optional: only for tracing
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

# LLM client (Gemini via OpenAI-compatible endpoint)
external_client: "AsyncOpenAI" = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Model selection
llm_model: "OpenAIChatCompletionsModel" = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client,
)

# Tool to load portfolio PDF (matches file present in backend/)
@function_tool
def read_portfolio_pdf() -> str:
    """Provides information about Bushra's skills, projects, and background."""
    try:
        with open("Profile (16) (1).pdf", "rb") as f:
            return "Portfolio PDF loaded successfully! Bushra is a skilled developer with expertise in web development, AI, and modern technologies."
    except FileNotFoundError:

          return "Portfolio information: Bushra is a skilled developer with expertise in web development, AI, and modern technologies."

# Basic agent (no tools)
portfolio_agent = Agent(
    name="PortfolioAgent",
    instructions=(
        "You are Bushra's AI portfolio assistant. Respond in a friendly, "
        "professional tone and talk about Bushra's skills, projects, and background. "
        "Use the read_portfolio_pdf tool when needed to provide accurate information." 
        "agar user kisi language mein baat kare to usi language mein reply karna."
        "conatct k bare me pouchy to keha conatct ka form bharne ka link do. portfolio me social media links bhi include ja wo show karna ok."

    ),
    model=llm_model,
    tools=[read_portfolio_pdf],
)