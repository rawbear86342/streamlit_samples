import streamlit as st
import random
import datetime
import time
import sqlite3
import ast

# Mock LLM response and citation functions (replace with your actual LLM)
def generate_mock_response(query):
    processing_placeholder = st.empty()
    processing_placeholder.write("Processing...")
    time.sleep(2)
    responses = [
        f"Mock response to: '{query}'.",
        "Here's some info.",
        "Response generated.",
    ]
    response = random.choice(responses)
    processing_placeholder.write(response)
    return response

def generate_mock_citations(response):
    citations = [
        {"source": "Source A", "page": "123"},
        {"source": "Source B", "page": "456"},
        {"source": "Source C", "page": "789"},
    ]
    return random.sample(citations, random.randint(0, len(citations)))

# Database functions
def create_connection():
    return sqlite3.connect("chat_history.db")

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            chat_id TEXT PRIMARY KEY,
            chat_data TEXT,
            citations_data TEXT
        )
    """)
    conn.commit()

def save_chat(conn, chat_id, chat_data, citations_data):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO chats (chat_id, chat_data, citations_data)
        VALUES (?, ?, ?)
    """, (chat_id, str(chat_data), str(citations_data)))
    conn.commit()

def load_chat(conn, chat_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT chat_data, citations_data FROM chats WHERE chat_id = ?
    """, (chat_id,))
    result = cursor.fetchone()
    if result:
        chat_data = ast.literal_eval(result[0])
        citations_data = ast.literal_eval(result[1])
        return chat_data, citations_data
    return None, None

# Initialize session state
if "chat_id" not in st.session_state:
    st.session_state.chat_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
if "message_citations" not in st.session_state:
    st.session_state.message_citations = {}

conn = create_connection()
create_table(conn)

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
    cursor = conn.cursor()
    cursor.execute('SELECT chat_id FROM chats')
    result = cursor.fetchall()
    for row in result:
        chat_data, citations_data = load_chat(conn, row[0])
        if chat_data:
            st.session_state.all_chats[row[0]] = chat_data
            if citations_data:
                st.session_state.message_citations[row[0]] = citations_data

if "current_chat" not in st.session_state:
    st.session_state.current_chat = st.session_state.all_chats.get(st.session_state.chat_id, [])
    if st.session_state.chat_id in st.session_state.message_citations:
        st.session_state.message_citations = st.session_state.message_citations[st.session_state.chat_id]
    else:
        st.session_state.message_citations = {}

# Sidebar for new chats and chat history
st.sidebar.title("Chat History")

if st.sidebar.button("➕ New Chat"):
    st.session_state.chat_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    st.session_state.current_chat = []
    st.session_state.message_citations = {}

for chat_id, chat in st.session_state.all_chats.items():
    if st.sidebar.button(f"Chat {chat_id}"):
        st.session_state.current_chat = chat
        st.session_state.chat_id = chat_id
        if chat_id in st.session_state.message_citations:
            st.session_state.message_citations = st.session_state.message_citations[chat_id]
        else:
            st.session_state.message_citations = {}

# Chat window
st.title("LLM Chat Bot")

for i, message in enumerate(st.session_state.current_chat):
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message["role"] == "assistant" and i in st.session_state.message_citations.get(st.session_state.chat_id, {}):
            with st.expander("Citations"):
                for citation in st.session_state.message_citations[st.session_state.chat_id][i]:
                    st.markdown(f"- {citation['source']}, page {citation['page']}")

if prompt := st.chat_input("Enter your message"):
    st.session_state.current_chat.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = generate_mock_response(prompt)
    citations = generate_mock_citations(response)
    st.session_state.current_chat.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

    if st.session_state.chat_id not in st.session_state.message_citations:
        st.session_state.message_citations[st.session_state.chat_id] = {}
    st.session_state.message_citations[st.session_state.chat_id][len(st.session_state.current_chat) - 1] = citations

    with st.chat_message("assistant"):
        with st.expander("Citations"):
            for citation in citations:
                st.markdown(f"- {citation['source']}, page {citation['page']}")

    st.session_state.all_chats[st.session_state.chat_id] = st.session_state.current_chat
    save_chat(conn, st.session_state.chat_id, st.session_state.current_chat, st.session_state.message_citations.get(st.session_state.chat_id, {}))

conn.close()
