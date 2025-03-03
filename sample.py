import streamlit as st

# Mock chat history data with user prompt, system response, and citation
chat_history = [
    {
        "id": 1,
        "timestamp": "2025-03-02 10:00",
        "user_prompt": "Extract the contract term and payment terms from the document.",
        "system_response": "Contract Term: 12 months from effective date.\nPayment Terms: Net 30 days from invoice.",
        "citations": ["[2023, 3, 5-8]", "[2023, 4, 12-15]"],
    }
]

# Streamlit UI
st.set_page_config(layout="wide")
st.title("📜 Contract Query App")
st.write("### Chat History")

# Vertical scrollable timeline
with st.container():
    for event in chat_history:
        with st.expander(f"{event['timestamp']} - Query #{event['id']}"):
            st.markdown(f"**User Prompt:** {event['user_prompt']}")
            st.markdown(f"**System Response:** {event['system_response']}")
            st.markdown(f"**Citations:** {', '.join(event['citations'])}")
