from agents import Agent, Runner, trace

from projectFunctions import send_email
from geminiModel import gemini_model
from agenticTools import tool1, tool2, tool3
from inputGuardrail import guardrail_against_name

tools = [tool1, tool2, tool3, send_email]

instructions ="You are a sales manager working for ComplAI. You use the tools given to you to generate cold sales emails. \
You never generate sales emails yourself; you always use the tools. \
You try all 3 sales_agent tools once before choosing the best one. \
You pick the single best email and use the send_email tool to send the best email (and only the best email) to the user."

sales_manager = Agent(
    name="Sales Manager", 
    instructions=instructions, 
    tools=tools, 
    model=gemini_model,
    input_guardrails=[guardrail_against_name]
    )

async def sales_manager_email(message = "Send a cold sales email addressed to 'Dear CEO'"):
    with trace("Sales manager"):
        result = await Runner.run(sales_manager, message)