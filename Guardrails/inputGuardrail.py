from agents import input_guardrail, Runner, GuardrailFunctionOutput, Agent, output_guardrail
from pydantic import BaseModel
from Model.geminiModel import gemini_model

class NameCheckOutput(BaseModel):
    is_name_in_message: bool
    name: str

guardrail_agent = Agent( 
    name="Name check",
    instructions="Check if the user is including someone's recivers and senders personal name in what they want you to do.",
    output_type=NameCheckOutput,
    model= gemini_model
)

@input_guardrail
async def guardrail_against_name(ctx, agent, message):
    result = await Runner.run(guardrail_agent, message, context=ctx.context)
    tigger = not result.final_output.is_name_in_message
    return GuardrailFunctionOutput(output_info={"found_name": result.final_output},tripwire_triggered= tigger)

