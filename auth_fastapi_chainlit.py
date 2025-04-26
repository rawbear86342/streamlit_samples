import chainlit as cl
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
import httpx
import os

# Ping Identity OIDC Configuration
PING_CLIENT_ID = "your_client_id"
PING_CLIENT_SECRET = "your_client_secret"
PING_AUTH_ENDPOINT = "https://your-ping-instance.com/as/authorization.oauth2"
PING_TOKEN_ENDPOINT = "https://your-ping-instance.com/as/token.oauth2"
PING_USERINFO_ENDPOINT = "https://your-ping-instance.com/idp/userinfo.openid"
REDIRECT_URI = "http://localhost:5000/login/callback"

# Store authorized users (this is a simple example)
user_sessions = {}

# FastAPI app for auth
fastapi_app = FastAPI()

@fastapi_app.get("/login")
def login():
    auth_url = (
        f"{PING_AUTH_ENDPOINT}?response_type=code"
        f"&client_id={PING_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=openid email profile"
    )
    return RedirectResponse(auth_url)

@fastapi_app.get("/login/callback")
async def login_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return HTMLResponse("<h1>Login failed: No code received</h1>")

    async with httpx.AsyncClient() as client:
        # Exchange code for tokens
        token_response = await client.post(
            PING_TOKEN_ENDPOINT,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "client_id": PING_CLIENT_ID,
                "client_secret": PING_CLIENT_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            return HTMLResponse(f"<h1>Token error: {token_data}</h1>")

        # Get user info
        userinfo_response = await client.get(
            PING_USERINFO_ENDPOINT,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_info = userinfo_response.json()
        email = user_info.get("email")

        if email:
            # Save session to in-memory store (or persistent store in production)
            user_sessions[email] = {
                "access_token": access_token,
                "user_info": user_info,
            }
            return HTMLResponse(f"<h1>Login successful: {email}</h1><p>You can now use the chat UI.</p>")
        else:
            return HTMLResponse(f"<h1>Failed to fetch user info</h1>")

# Chainlit integration with FastAPI
@cl.set_fastapi_app
def get_fastapi_app():
    return fastapi_app

# Main Chainlit chat logic
@cl.on_message
async def on_message(message: cl.Message):
    # You can modify this to verify against actual session cookies or headers
    # For demo: use hardcoded allowed email
    allowed_email = next(iter(user_sessions), None)

    if not allowed_email:
        await cl.Message(content="❌ Please log in at http://localhost:5000/login").send()
        return

    email = allowed_email
    user_info = user_sessions[email]
    await cl.Message(content=f"👋 Hello {user_info['user_info']['email']}! You said: {message.content}").send()
