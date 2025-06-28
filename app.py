from agents import Agent, Runner, trace
import asyncio

from Tools.projectFunctions import send_email, not_answered
from Model.geminiModel import gemini_model
from Agents.agenticTools import tool1, tool2, tool3
from Guardrails.inputGuardrail import guardrail_against_name
from Guardrails.spamGuardrail import guardrail_against_spam
from RagSearch.query_chroma_db import ragTool
from Tools.MongoData import run_mongo_command
from Agents.DBtool import mongoQueryTool
tools = [tool1, tool2, tool3, send_email]

instructions_sales ="""
You are a sales manager working for ComplAI. You use the tools given to you to generate cold sales emails.
You never generate sales emails yourself; you always use the tools.
You try all 3 sales_agent tools once before choosing the best one.
You pick the single best email and use the send_email tool to send the best email (and only the best email) to the user."""

instructions_manager = """
aboutComplAi: ComplAi is a Saas company providing tools to help with customer call service as ai customer support.
You are email manager working for ComplAI. 
You decide the type of mail give to you and handoff to the agent based on that
Query kind of mail where user asking about some info handoffs to query_reply
or mail to order handoffs to query_reply """

instructions_query = """
"You generate reply mails"
📝 Your role is to:
- Receive and understand user questions or information requests.
- Uses a rag tool 'ragTool' to gether information about it
- Craft a helpful and relevant reply.
- Once the reply is written, use the `send_mail` tool to send the response to the user.
- If you dont know about the ANSWER, use the not_answered tool sending it query in one line with remarks not answered

🖊️ Signature Rule:
- At the end of the reply, always include: **"© All rights reserved – ComplAIQuery."**
"""

instructions_order = """
You have to use tools to get the the database reponse as list and understand user query , then handoff these to another agent, its must to use run_mongo_command mongoQueryTool tools only then you can reply
📝 steps you should follow:
- Receive and understand user questions or information requests.
- (must do step) use the 'mongoQueryTool' tool agent to create a Query based on what user asked
- (must do step) Then use the tool 'run_mongo_command' to call the query and get the response
- then you uses convert the tool reponse into  make the reponse understandable 
- costomize the reply based on the data/content you have recived 
- (must do step) use the tool 'send_email' to send you response to the mail
- if you find difficulty anywhere use the tool not_answered to log you difficulty
🖊️ Signature Rule:
- You never create query yourself always use tool 

"""


sales_manager = Agent(
    name="Sales Manager", 
    instructions=instructions_sales, 
    tools=tools, 
    model=gemini_model,
    input_guardrails=[guardrail_against_name]
)

reply_agents_manager = Agent(
    name = "Agents Manager",
    instructions=instructions_manager, 
    model=gemini_model,
    input_guardrails=[guardrail_against_spam],
    handoffs = [order_reply , query_reply]
)

query_reply = Agent(
    name="replies query",
    instructions= instructions_query,
    tools = [send_email, not_answered,ragTool],
    handoff_description="answers queries",
    model = gemini_model
)

order_reply = Agent(
    name="DB QUERY RESOLVE",
    instructions= instructions_order,
    tools = [send_email,mongoQueryTool,run_mongo_command,not_answered],
    model = gemini_model
)



async def email_generator(type = "Query", message = "I want to know about AVG FEES BY COURSES"):
    if type == "Sales" :
        print("processing your sales mail......")
        with trace("Sales Agent workflow"):
            await Runner.run(sales_manager, message) 
    else:
        print("processing reply mails......")
        with trace("Reply Agent workflow"):
            result = await Runner.run(reply_agents_manager, message)

asyncio.run(email_generator())