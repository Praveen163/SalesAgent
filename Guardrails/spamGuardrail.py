from agents import input_guardrail, Runner, GuardrailFunctionOutput, Agent, output_guardrail
from pydantic import BaseModel
from Model.geminiModel import gemini_model

#GUARDRAIL2
class SpamCheck(BaseModel):
    is_geniune_mail: bool

spam_guardrail_agent = Agent( 
    name="SPAM check",
    instructions="Check if the QUERY is not a spam mail its a geniune query mail or the order realated mail.",
    output_type=SpamCheck,
    model= gemini_model
)

@input_guardrail
async def guardrail_against_spam(ctx, agent, message):
    result = await Runner.run(spam_guardrail_agent, message, context=ctx.context)
    tigger = not result.final_output.is_geniune_mail
    return GuardrailFunctionOutput(output_info={"found_name": result.final_output},tripwire_triggered= tigger)