import streamlit as st
import os
import secrets
import urllib.parse
import requests
from authlib.integrations.requests_client import OAuth2Session
from dotenv import load_dotenv

load_dotenv()

# Load config
client_id = os.getenv("OAUTH_CLIENT_ID")
client_secret = os.getenv("OAUTH_CLIENT_SECRET")
authorize_url = os.getenv("OAUTH_AUTHORIZATION_ENDPOINT")
token_url = os.getenv("OAUTH_TOKEN_ENDPOINT")
userinfo_url = os.getenv("OAUTH_USERINFO_ENDPOINT")
redirect_uri = os.getenv("OAUTH_REDIRECT_URI")
scope = os.getenv("OAUTH_SCOPE", "openid")

# Store session
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None

st.markdown(f'<meta http-equiv="refresh" content="0;url={login_url()}">', unsafe_allow_html=True)
st.stop()

def login_url():
    state = secrets.token_urlsafe(16)
    st.session_state['state'] = state
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state,
    }
    return f"{authorize_url}?{urllib.parse.urlencode(params)}"

def exchange_code_for_token(code):
    session = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri)
    token = session.fetch_token(
        token_url=token_url,
        code=code,
    )
    return token

def get_user_info(token):
    headers = {"Authorization": f"Bearer {token['access_token']}"}
    resp = requests.get(userinfo_url, headers=headers)
    return resp.json()

# Handle OAuth redirect with code
query_params = st.experimental_get_query_params()
if "code" in query_params and "state" in query_params:
    if query_params["state"][0] != st.session_state.get("state"):
        st.error("State mismatch. Possible CSRF detected.")
    else:
        try:
            token = exchange_code_for_token(query_params["code"][0])
            user = get_user_info(token)
            st.session_state.token = token
            st.session_state.user = user
            # Cleanup URL
            st.experimental_set_query_params()
        except Exception as e:
            st.error(f"Login failed: {str(e)}")

# Show user info or login
if st.session_state.user:
    st.success(f"Welcome, {st.session_state.user.get('name', 'user')} 👋")
    st.write("🔐 Profile:", st.session_state.user)
    # Your secure chat app starts here
    st.text_input("Say something:")
else:
    st.title("🔐 Secure Login with PingFederate")
    st.markdown("Please log in with your PingFederate SSO provider.")
    st.link_button("Login with PingFederate", login_url())
