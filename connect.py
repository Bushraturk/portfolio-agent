

# new


import os
from typing import Any
from dotenv import load_dotenv, find_dotenv
from agents import GuardrailFunctionOutput, input_guardrail, output_guardrail, RunContextWrapper
from agentsapp import portfolio_agent, external_client, llm_model  # re-exported if needed

_ = load_dotenv(find_dotenv())

@input_guardrail
async def portfolio_input_checker(ctx: RunContextWrapper, agent: portfolio_agent, input):
    # Allow all inputs for now
    return GuardrailFunctionOutput(
        output_info="passed",
        tripwire_triggered=False,
    )

@output_guardrail
def portfolio_response_checker(ctx: RunContextWrapper, agent: portfolio_agent, output: Any):
    # Allow all outputs for now
    return GuardrailFunctionOutput(
        output_info="passed",
        tripwire_triggered=False,
    )