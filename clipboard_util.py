import streamlit as st

def copy_to_clipboard_button(text, key):
    """Adds a copy button to each response or prompt"""
    copy_script = f"""
    <script>
    function copyToClipboard(text) {{
        navigator.clipboard.writeText(text).then(function() {{
            console.log('Copied to clipboard:', text);
        }}, function(err) {{
            console.error('Could not copy text:', err);
        }});
    }}
    </script>
    <button onclick="copyToClipboard('{text.replace("'", "\\'")}')">📋 Copy</button>
    """
    st.markdown(copy_script, unsafe_allow_html=True)

# Example usage:
st.title("💬 Chat with Copy Button")

# Simulating chat messages
chat_messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I'm an AI assistant. How can I help?"}
]

for i, msg in enumerate(chat_messages):
    with st.chat_message(msg["role"]):
        st.text_area(f"Message {i}", msg["content"], height=50, key=f"msg_{i}", disabled=True)
        copy_to_clipboard_button(msg["content"], f"copy_{i}")
