# app.py - Combined Flask + Streamlit application

import os
import json
import time
import requests
import urllib.parse
import threading
import webbrowser
import uuid
from flask import Flask, request, redirect, session, jsonify
import streamlit as st
import streamlit.web.bootstrap as bootstrap
import streamlit.web.server as server
from werkzeug.security import generate_password_hash, check_password_hash

# Ping Identity configuration
PING_CLIENT_ID = "your_client_id"
PING_CLIENT_SECRET = "your_client_secret"
PING_AUTH_ENDPOINT = "https://your-ping-instance.com/as/authorization.oauth2"
PING_TOKEN_ENDPOINT = "https://your-ping-instance.com/as/token.oauth2"
PING_USERINFO_ENDPOINT = "https://your-ping-instance.com/idp/userinfo.openid"
REDIRECT_URI = "http://localhost:5000/login/callback"

# Session storage - in production use Redis or another shared session store
session_store = {}

# Create Flask app for handling routes
flask_app = Flask(__name__)
flask_app.secret_key = os.urandom(24)

@flask_app.route("/")
def index():
    # Redirect to Streamlit on the main route
    return redirect("http://localhost:8501")

@flask_app.route("/login")
def login():
    # Create a session ID that will be used to pass data between Flask and Streamlit
    session_id = str(uuid.uuid4())
    session_store[session_id] = {"created_at": time.time()}
    
    # Construct the authorization URL with state parameter
    params = {
        'client_id': PING_CLIENT_ID,
        'response_type': 'code',
        'scope': 'openid profile email',
        'redirect_uri': REDIRECT_URI,
        'state': session_id  # Pass session ID as state parameter
    }
    
    auth_url = f"{PING_AUTH_ENDPOINT}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

@flask_app.route("/login/callback")
def callback():
    # Handle the callback from Ping Identity
    code = request.args.get("code")
    state = request.args.get("state")  # Retrieve the session ID
    
    if not state or state not in session_store:
        return "Invalid session", 400
        
    if code:
        # Exchange authorization code for tokens
        token_payload = {
            'grant_type': 'authorization_code',
            'client_id': PING_CLIENT_ID,
            'client_secret': PING_CLIENT_SECRET,
            'code': code,
            'redirect_uri': REDIRECT_URI
        }
        
        token_response = requests.post(PING_TOKEN_ENDPOINT, data=token_payload)
        
        if token_response.status_code == 200:
            tokens = token_response.json()
            
            # Get user info with the access token
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            userinfo_response = requests.get(PING_USERINFO_ENDPOINT, headers=headers)
            
            if userinfo_response.status_code == 200:
                user_info = userinfo_response.json()
                
                # Store authentication data in the session store
                session_store[state].update({
                    "authenticated": True,
                    "tokens": tokens,
                    "user_info": user_info,
                    "last_accessed": time.time()
                })
                
                # Redirect to Streamlit with the session ID
                return redirect(f"http://localhost:8501/?session_id={state}")
            else:
                return f"Failed to get user info: {userinfo_response.text}", 400
        else:
            return f"Authentication failed: {token_response.text}", 400
    else:
        return "No authorization code provided", 400

@flask_app.route("/api/auth-status")
def auth_status():
    # API endpoint for Streamlit to check authentication status
    session_id = request.args.get("session_id")
    
    if session_id and session_id in session_store:
        # Clean sensitive data before sending
        auth_data = session_store[session_id].copy()
        if "tokens" in auth_data:
            # Only return necessary token info and user info
            safe_data = {
                "authenticated": auth_data.get("authenticated", False),
                "username": auth_data.get("user_info", {}).get("preferred_username", ""),
                "email": auth_data.get("user_info", {}).get("email", ""),
                "name": auth_data.get("user_info", {}).get("name", ""),
                "last_accessed": auth_data.get("last_accessed", 0)
            }
            # Update last accessed time
            session_store[session_id]["last_accessed"] = time.time()
            return jsonify(safe_data)
    
    return jsonify({"authenticated": False})

@flask_app.route("/logout")
def logout():
    # Handle logout
    session_id = request.args.get("session_id")
    if session_id and session_id in session_store:
        session_store.pop(session_id, None)
    
    return redirect("http://localhost:8501")

# Define the Streamlit part of the application
def streamlit_app():
    st.title("Ping Identity Integration")
    
    # Check for session ID in query parameters
    query_params = st.experimental_get_query_params()
    session_id = query_params.get("session_id", [""])[0]
    
    if "auth_status" not in st.session_state:
        st.session_state.auth_status = {"authenticated": False}
    
    # If there's a session ID, check authentication status
    if session_id:
        try:
            # Get authentication status from Flask API
            response = requests.get(f"http://localhost:5000/api/auth-status?session_id={session_id}")
            if response.status_code == 200:
                st.session_state.auth_status = response.json()
                st.session_state.session_id = session_id
            else:
                st.error("Failed to verify authentication status")
        except Exception as e:
            st.error(f"Error checking authentication: {e}")
    
    # Display user information if authenticated
    if st.session_state.auth_status.get("authenticated"):
        st.success(f"Welcome, {st.session_state.auth_status.get('name', 'User')}!")
        st.write(f"Email: {st.session_state.auth_status.get('email', '')}")
        
        # Main application content here
        st.header("Your Dashboard")
        st.write("This is your protected application content.")
        
        # Logout button
        if st.button("Logout"):
            logout_url = f"http://localhost:5000/logout?session_id={st.session_state.session_id}"
            webbrowser.open(logout_url)
            st.session_state.auth_status = {"authenticated": False}
            st.experimental_set_query_params()
            st.experimental_rerun()
    else:
        st.warning("You are not authenticated")
        st.write("Click the button below to authenticate with Ping Identity")
        
        if st.button("Login with Ping Identity"):
            webbrowser.open("http://localhost:5000/login")

def run_flask():
    flask_app.run(port=5000)

def run_streamlit():
    server.address = "localhost"
    server.port = 8501
    bootstrap.run(streamlit_app, "", args=[], flag_options={})

# Clean up old sessions periodically
def cleanup_sessions():
    while True:
        current_time = time.time()
        expired_sessions = [sid for sid, data in session_store.items() 
                           if current_time - data.get("last_accessed", data.get("created_at", 0)) > 3600]
        for sid in expired_sessions:
            session_store.pop(sid, None)
        time.sleep(300)  # Check every 5 minutes

if __name__ == "__main__":
    # Start session cleanup in a separate thread
    cleanup_thread = threading.Thread(target=cleanup_sessions)
    cleanup_thread.daemon = True
    cleanup_thread.start()
    
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Run Streamlit in the main thread
    run_streamlit()
