# chainlit.config.py

import chainlit as cl
import requests

PINGFEDERATE_USERINFO_ENDPOINT = "https://your-pingfederate.example.com/as/userinfo.oauth2"

@cl.on_auth
async def on_auth(auth_request: cl.AuthRequest):
    """
    Handle authentication via PingFederate SSO by verifying bearer token.
    """
    token = auth_request.access_token

    if not token:
        raise cl.UnauthorizedError("No access token provided. Please login via SSO.")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(PINGFEDERATE_USERINFO_ENDPOINT, headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        user_identity = user_info.get("sub") or user_info.get("email") or "unknown-user"
        return cl.User(identifier=user_identity)
    else:
        raise cl.UnauthorizedError(f"Invalid access token. PingFederate error: {response.text}")
