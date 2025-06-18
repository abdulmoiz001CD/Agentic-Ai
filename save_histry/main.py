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

@cl.on_chat_start
async def handle_chat():
    cl.user_session.set("history",[])
    await cl.Message(content= "Hello! , I am a Panaversty Support Agent").send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")
    
    history.append({"role":"user", "content": message.content})

    result = await Runner.run(
        agent_pana,
        input=history,
        run_config= config,
    )
    history.append({"role":"assistant","content": result.final_output})
    cl.user_session.set("history",history)
    await cl.Message(content= result.final_output).send()