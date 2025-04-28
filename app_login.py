import chainlit as cl
import os
from starlette.responses import HTMLResponse
from starlette.requests import Request

# Serve your own index.html
@cl.on_before_server_start
async def setup_server(app):
    @app.get("/")
    async def custom_root(request: Request):
        # Serve custom index.html for SSO login
        with open(os.path.join(os.path.dirname(__file__), "public/index.html")) as f:
            content = f.read()
        return HTMLResponse(content=content)

@cl.on_message
async def on_message(message: cl.Message):
    await cl.Message(content=f"Hello {message.author}! You said: {message.content}").send()
