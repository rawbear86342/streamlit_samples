# app.py
import chainlit as cl

@cl.on_message
async def on_message(message: cl.Message):
    await cl.Message(content=f"Hello {message.author}! You said: {message.content}").send()
