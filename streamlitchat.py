import streamlit as st
import datetime
import sqlite3
import random
import time
import ast

# 🔹 Default System Prompt
DEFAULT_SYSTEM_PROMPT = "You are an AI assistant. Provide clear and concise responses."

# 📌 Database setup
def create_connection():
    return sqlite3.connect("chat_history.db", check_same_thread=False)

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            chat_id TEXT PRIMARY KEY,
            chat_data TEXT,
            citations_data TEXT,
            feedback_data TEXT
        )
    """)
    conn.commit()

# 📌 Save and load chat history
def save_chat(conn, chat_id, chat_data, citations_data, feedback_data):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO chats (chat_id, chat_data, citations_data, feedback_data)
        VALUES (?, ?, ?, ?)
    """, (chat_id, str(chat_data), str(citations_data), str(feedback_data)))
    conn.commit()

def load_chat(conn, chat_id):
    cursor = conn.cursor()
    cursor.execute("SELECT chat_data, citations_data, feedback_data FROM chats WHERE chat_id = ?", (chat_id,))
    result = cursor.fetchone()
    if result:
        try:
            chat_data = ast.literal_eval(result[0]) if result[0] else []
            citations_data = ast.literal_eval(result[1]) if result[1] else {}
            feedback_data = ast.literal_eval(result[2]) if result[2] else {}
            return chat_data, citations_data, feedback_data
        except Exception:
            return [], {}, {}
    return [], {}, {}

# 📌 Mock AI response and citation generator
def generate_mock_response(query):
    time.sleep(1)  # Simulating processing delay
    responses = [
        f"Here's an AI-generated response to: '{query}'.",
        "I found something useful!",
        "This might help with your question."
    ]
    return random.choice(responses)

def generate_mock_citations():
    sources = [
        {"source": "AI Research Paper", "page": "23"},
        {"source": "Tech Blog", "page": "45"},
        {"source": "Journal of AI", "page": "78"}
    ]
    return random.sample(sources, random.randint(1, len(sources)))

# 📌 Streamlit setup
st.set_page_config(page_title="AI Chat with Feedback", layout="wide")

# 📌 Session state initialization
conn = create_connection()
create_table(conn)

if "chat_id" not in st.session_state:
    st.session_state.chat_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

if "chat_history" not in st.session_state:
    chat_data, citations_data, feedback_data = load_chat(conn, st.session_state.chat_id)
    st.session_state.chat_history = chat_data if chat_data else []
    st.session_state.citations = citations_data if citations_data else {}
    st.session_state.feedback = feedback_data if feedback_data else {}

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT

conn.close()

# 📌 Sidebar - Chat history & system prompt customization
st.sidebar.title("Chat History")
if st.sidebar.button("➕ New Chat"):
    st.session_state.chat_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    st.session_state.chat_history = []
    st.session_state.citations = {}
    st.session_state.feedback = {}
    st.session_state.uploaded_files = []
    st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT

# 🔹 Editable System Prompt
st.sidebar.markdown("### 🛠️ System Prompt")
st.session_state.system_prompt = st.sidebar.text_area("Modify System Prompt:", st.session_state.system_prompt)

# 📌 Layout - Two-column chat + upload section
col1, col2 = st.columns([3, 1])

with col1:
    st.title("💬 AI Chat with Feedback & Citations")

    # 📌 Display chat messages
    for i, message in enumerate(st.session_state.chat_history):
        with st.chat_message(message["role"]):
            # Display content and timestamp together
            if message.get("timestamp"):
                st.markdown(f"{message['content']} *<span style='color: #888; font-size: 0.8em;'>({message['timestamp']})</span>*", unsafe_allow_html=True)
            else:
                st.write(message["content"])

            if message["role"] == "assistant":
                # 📖 Show citations
                if i in st.session_state.citations:
                    with st.expander("📚 Citations"):
                        for citation in st.session_state.citations[i]:
                            st.markdown(f"- {citation['source']}, page {citation['page']}")

                # 👍👎 Human Feedback (Thumbs Up/Down) appears immediately
                feedback_key = f"feedback_{i}"
                feedback_options = ["👍", "👎"]
                current_feedback = st.session_state.feedback.get(i, None)

                new_feedback = st.radio(
                    "Was this response helpful?",
                    feedback_options,
                    index=feedback_options.index(current_feedback) if current_feedback in feedback_options else None,
                    key=feedback_key,
                    horizontal=True
                )

                # 📌 Store feedback & Save to Database
                if new_feedback and new_feedback != current_feedback:
                    st.session_state.feedback[i] = new_feedback

                    # 🔹 Save feedback to the database
                    conn = create_connection()
                    save_chat(conn, st.session_state.chat_id, st.session_state.chat_history, st.session_state.citations, st.session_state.feedback)
                    conn.close()

with col2:
    # 📌 📂 Subtle Upload section
    st.markdown("### 📁 Upload Files")

    uploaded_file = st.file_uploader("Click to upload a file", type=["txt", "pdf", "docx"], label_visibility="collapsed")
    
    if uploaded_file:
        file_size_mb = uploaded_file.size / (1024 * 1024)  # Convert bytes to MB
        st.session_state.uploaded_files.append({"name": uploaded_file.name, "size": round(file_size_mb, 2)})
        st.experimental_rerun()

    # 📌 Show uploaded files with sleek display
    for file_data in st.session_state.uploaded_files:
        st.write(f"📄 {file_data['name']} ({file_data['size']} MB)")

# 📌 💬 Chat Input (Anchored to Bottom)
prompt = st.chat_input("Enter your message...")

if prompt:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 📌 Display user message
    st.session_state.chat_history.append({"role": "user", "content": prompt, "timestamp": timestamp})
    st.chat_message("user").write(prompt)

    # 📌 Generate AI response
    response = generate_mock_response(prompt)
    citations = generate_mock_citations()
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.chat_history.append({"role": "assistant", "content": response, "timestamp": timestamp})
    st.session_state.citations[len(st.session_state.chat_history) - 1] = citations

    # 📌 Display AI response
    with st.chat_message("assistant"):
        st.markdown(f"{response} *<span style='color: #888; font-size: 0.8em;'>({timestamp})</span>*", unsafe_allow_html=True)

        # 📌 Display citations
        with st.expander("📚 Citations"):
            for citation in citations:
                st.markdown(f"- {citation['source']}, page {citation['page']}")

        # 📌 Show Feedback UI immediately
        feedback_key = f"feedback_{len(st.session_state.chat_history) - 1}"
        st.radio("Was this response helpful?", ["👍", "👎"], key=feedback_key, horizontal=True)

    # 📌 Save chat history
    conn = create_connection()
    save_chat(conn, st.session_state.chat_id, st.session_state.chat_history, st.session_state.citations, st.session_state.feedback)
    conn.close()
