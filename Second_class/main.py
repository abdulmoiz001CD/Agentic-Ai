import chainlit as cl

@cl.on_chat_start
def on_chat_start():
   print("Hello Buddy")

@cl.on_message
async def main(message: cl.Message):

    await cl.Message(
        content=f"The User Sent: {message.content}",
    ).send()

@cl.on_chat_end
def on_chat_end():
    print(f'The user disconnected')
