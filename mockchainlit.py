import chainlit as cl
import uuid
from typing import List, Dict
from datetime import datetime
import random
import sqlite3

class ChatManager:
    def __init__(self, db_path="chat_history.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                session_id TEXT,
                query TEXT,
                response TEXT,
                timestamp TEXT
            )
        """)
        self.conn.commit()

    def create_session(self, session_id: str = None):
        if not session_id:
            session_id = str(uuid.uuid4())
        return session_id

    def add_message(self, session_id: str, query: str, response: str):
        timestamp = datetime.now().isoformat()
        self.cursor.execute("""
            INSERT INTO chat_history (session_id, query, response, timestamp)
            VALUES (?, ?, ?, ?)
        """, (session_id, query, response, timestamp))
        self.conn.commit()

    def get_chat_history(self, session_id: str) -> List[Dict]:
        self.cursor.execute("""
            SELECT query, response, timestamp
            FROM chat_history
            WHERE session_id = ?
            ORDER BY timestamp
        """, (session_id,))
        rows = self.cursor.fetchall()
        return [{"query": row[0], "response": row[1], "timestamp": row[2]} for row in rows]

    def close(self):
        self.conn.close()

chat_manager = ChatManager()

def generate_mock_response(query: str) -> str:
    responses = [
        f"Sure, here's a mock response to '{query}'.",
        f"Let me think... '{query}' is an interesting topic.",
        f"I'm processing your request for '{query}'.",
        f"Here's some information related to '{query}'.",
        f"Based on your query '{query}', here's what I came up with.",
    ]
    return random.choice(responses)

@cl.on_chat_start
async def start():
    session_id = chat_manager.create_session()
    cl.user_session.set("session_id", session_id)
    await cl.Message(
        content="👋 Welcome! I'm your AI assistant. Ready to help you with any questions or tasks."
    ).send()
    
    # Create a sidebar element
    await cl.Sidebar(
        name="Chat History",
        content=""
    ).send()

@cl.on_message
async def main(message: cl.Message):
    session_id = cl.user_session.get("session_id")
    response_text = generate_mock_response(message.content)
    
    # Send messages
    await cl.Message(content=response_text).send()
    chat_manager.add_message(session_id, message.content, response_text)
    
    # Update sidebar
    history = chat_manager.get_chat_history(session_id)
    sidebar_content = "\n\n".join([
        f"**User:** {entry['query']}\n**Assistant:** {entry['response']}"
        for entry in history
    ])
    
    # Send sidebar update
    await cl.Sidebar(
        name="Chat History",
        content=sidebar_content
    ).send()

@cl.on_chat_resume
async def resume(resume_token: str):
    session_id = resume_token
    cl.user_session.set("session_id", session_id)
    history = chat_manager.get_chat_history(session_id)

    for chat_entry in history:
        await cl.Message(
            content=f"**User:** {chat_entry['query']}\n\n**Assistant:** {chat_entry['response']}"
        ).send()
    
    # Update sidebar with existing history
    sidebar_content = "\n\n".join([
        f"**User:** {entry['query']}\n**Assistant:** {entry['response']}"
        for entry in history
    ])
    
    await cl.Sidebar(
        name="Chat History",
        content=sidebar_content
    ).send()

def configure():
    cl.config.ui.name = "Enhanced Chat Assistant"
    cl.config.ui.description = "Intelligent conversation interface"
    cl.config.ui.show_thought = True
    cl.config.ui.css = """
    .chainlit-chat-container {
        height: 80vh;
        overflow-y: auto;
    }
    .chainlit-user-message {
        transition: opacity 0.5s ease-in-out;
        opacity: 1;
    }
    .chainlit-user-message.faded-out {
        opacity: 0;
    }
    """

if __name__ == "__main__":
    configure()

@cl.on_stop
def on_stop():
    chat_manager.close()
