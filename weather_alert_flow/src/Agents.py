from agents import (
    Agent, Runner, function_tool, 
    trace, input_guardrail, GuardrailFunctionOutput
)
from Instructions import weather_agent_instructions, guardrail_agent_instructions
from Models import WeatherGuardrailOutput, MailComponents

guardrail_agent = Agent(
    name="Guardrail_Checker",
    instructions=guardrail_agent_instructions,
    output_type=WeatherGuardrailOutput
)

@input_guardrail
async def validate_weather_request(ctx, agent, user_input):

    result = await Runner.run(
        guardrail_agent,
        input=user_input,
        context=ctx.context,
    )
    is_place_specified = result.final_output.is_place_specified
    output = result.final_output

    return GuardrailFunctionOutput(
        tripwire_triggered=not is_place_specified,
        output_info=output.place_name,
    )

def weather_agent(tools, model):

    weather_agent = Agent(
        name="Weather Assistant",
        instructions=weather_agent_instructions,
        tools=tools,
        model=f"{model}",
        input_guardrails=[validate_weather_request],
        output_type=MailComponents
    )
    return weather_agent