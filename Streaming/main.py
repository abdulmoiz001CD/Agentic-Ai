import os
from agents import Agent, Runner,ItemHelpers, AsyncOpenAI, OpenAIChatCompletionsModel,RunConfig
import random
from dotenv import load_dotenv
import chainlit as cl

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model= "gemini-2.0-flash",
    openai_client= external_client
)


config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent_pana = Agent(
    name = "Panaversity Support Agent",
    instructions="You area a Helpful assistant that can give answer questions",
    
)

@cl.on_message
async def handle_message(message: cl.Message):
    result = await Runner.run(
        agent_pana,
        input=message.content,
        run_config= config,
    )
    await cl.Message(content= result.final_output).send()