import streamlit as st

st.subheader("Review Data")

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("👍 Approve", key="approve"):
        st.success("You approved the data!")

with col2:
    if st.button("👎 Reject", key="reject"):
        st.error("You rejected the data!")

# Optional feedback input
if st.checkbox("Leave a comment"):
    feedback = st.text_area("Enter your feedback:")
    if st.button("Submit Feedback", key="submit_feedback"):
        st.write("Thank you for your feedback!")
        st.write(f"Feedback: {feedback}")
