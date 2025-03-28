import os
import json
import time
from cryptography.fernet import Fernet
import requests

TOKEN_FILE = ".token.enc"
SECRET_KEY_FILE = "secret.key"
TOKEN_EXPIRY_THRESHOLD = 3600  # 1 hour (in seconds)

# 🔹 Generate encryption key (Run once)
def generate_key():
    key = Fernet.generate_key()
    with open(SECRET_KEY_FILE, "wb") as key_file:
        key_file.write(key)
    print("🔑 Encryption key saved to 'secret.key'. Keep this safe!")

# 🔹 Load encryption key
def load_key():
    if not os.path.exists(SECRET_KEY_FILE):
        generate_key()
    return open(SECRET_KEY_FILE, "rb").read()

# 🔹 Encrypt token and save it securely
def save_token(token_data):
    key = load_key()
    cipher_suite = Fernet(key)
    
    encrypted_data = cipher_suite.encrypt(json.dumps(token_data).encode())
    with open(TOKEN_FILE, "wb") as enc_file:
        enc_file.write(encrypted_data)
    
    print("✅ Token encrypted and saved.")

# 🔹 Decrypt and load token data
def load_token():
    if not os.path.exists(TOKEN_FILE):
        return None
    
    key = load_key()
    cipher_suite = Fernet(key)
    
    with open(TOKEN_FILE, "rb") as enc_file:
        encrypted_data = enc_file.read()

    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return json.loads(decrypted_data)

# 🔹 Check if token is expiring soon
def is_token_expiring():
    token_data = load_token()
    if not token_data:
        return True  # No token found, must refresh

    expiry_time = token_data.get("expires_at", 0)
    remaining_time = expiry_time - time.time()
    
    print(f"⏳ Token expires in {remaining_time:.0f} seconds.")

    return remaining_time < TOKEN_EXPIRY_THRESHOLD

# 🔹 Fetch a new token from API (Simulated here)
def fetch_new_token():
    print("🔄 Fetching new token...")
    
    # Mock API call (Replace with actual API request)
    response = {
        "access_token": "new_generated_token_123",
        "expires_in": 7200  # 2 hours
    }

    # Compute expiry time
    expiry_time = time.time() + response["expires_in"]

    # Store token securely
    token_data = {"token": response["access_token"], "expires_at": expiry_time}
    save_token(token_data)

    return token_data

# 🔹 Get a valid token (Refresh if needed)
def get_valid_token():
    if is_token_expiring():
        return fetch_new_token()["token"]

    return load_token()["token"]

# 🛠 Usage Example
if __name__ == "__main__":
    valid_token = get_valid_token()
    print(f"🔐 Current Token: {valid_token}")
