from agents import Agent, Runner, trace
import asyncio

from projectFunctions import send_email, not_answered
from geminiModel import gemini_model
from agenticTools import tool1, tool2, tool3
from inputGuardrail import guardrail_against_name,guardrail_against_spam

tools = [tool1, tool2, tool3, send_email]

instructions ="You are a sales manager working for ComplAI. You use the tools given to you to generate cold sales emails. \
You never generate sales emails yourself; you always use the tools. \
You try all 3 sales_agent tools once before choosing the best one. \
You pick the single best email and use the send_email tool to send the best email (and only the best email) to the user."

instructions_manager = "\
aboutComplAi: ComplAi is a Saas company providing tools to help with customer call service as ai customer support.\
You are email manager working for ComplAI. \
You decide the type of mail give to you and handoff to the agent based on that\
Query kind of mail where user asking about some info handoffs to query_reply\
or mail to order handoffs to query_reply "

instructions_query = """
"You generate reply mails"
📝 Your role is to:
- Receive and understand user questions or information requests.
- Craft a helpful and relevant reply.
- Once the reply is written, use the `send_mail` tool to send the response to the user.
- If you dont know about the ANSWER, use the not_answered tool sending it query in one line with remarks not answered

🖊️ Signature Rule:
- At the end of the reply, always include: **"© All rights reserved – ComplAIQuery."**
"""

instructions_order = """You are the Order Response Agent at ComplAI.

📦 Your job is to:
- Handle all user emails that involve **orders, purchases, or sales-related requests**.
- Respond with appropriate confirmation, clarification, or details as per the order.

🖊️ Signature Rule:
- At the end of the reply, always include: **"© All rights reserved – ComplAIOrders."**

📤 Use the `send_mail` tool to deliver the email to the user once it's ready."""

sales_manager = Agent(
    name="Sales Manager", 
    instructions=instructions, 
    tools=tools, 
    model=gemini_model,
    input_guardrails=[guardrail_against_name]
)

query_reply = Agent(
    name="replies query",
    instructions= instructions_query,
    tools = [send_email, not_answered],
    handoff_description="answers queries",
    model = gemini_model
)

order_reply = Agent(
    name="Order Request",
    instructions= instructions_order,
    tools = [send_email],
    handoff_description="answers order requests",
    model = gemini_model
)

reply_agents_manager = Agent(
    name = "Agents Manager",
    instructions=instructions_manager, 
    model=gemini_model,
    input_guardrails=[guardrail_against_spam],
    handoffs = [order_reply , query_reply]
)

async def email_generator(type = "uhi", message = "I want to know about you"):
    if type == "Sales" :
        print("processing your sales mail......")
        await Runner.run(sales_manager, message) 
    else:
        print("processing reply mails......")
        result = await Runner.run(query_reply, message)
        # print(result.final_output)
asyncio.run(email_generator())