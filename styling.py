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


import streamlit as st

# Custom CSS for styling
st.markdown(
    """
    <style>
        /* Make the sidebar arrow invisible */
        .css-1f4v2d9 {
            display: none;
        }
        
        /* Make the sidebar background transparent */
        .css-1d391kg {
            background-color: transparent !important;
        }
        
        /* Optional: style sidebar header */
        .css-1hbfdn5 {
            background-color: transparent !important;
        }
        
        /* Optional: adjust text or other sidebar components */
        .css-1mcpo5g {
            color: #000;  /* Black text */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Your Streamlit app content

st.sidebar.header("Sidebar with Custom Styles")
st.sidebar.write("This is a transparent sidebar with no arrow.")




import streamlit as st

# Custom CSS for styling
st.markdown(
    """
    <style>
        /* Make the sidebar arrow invisible */
        .css-1f4v2d9 {
            display: none;
        }
        
        /* Make the sidebar background transparent */
        .css-1d391kg {
            background-color: transparent !important;
        }
        
        /* Optional: style sidebar header */
        .css-1hbfdn5 {
            background-color: transparent !important;
        }
        
        /* Optional: adjust text or other sidebar components */
        .css-1mcpo5g {
            color: #000;  /* Black text */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Your Streamlit app content
st.sidebar.header("Sidebar with Custom Styles")
st.sidebar.write("This is a transparent sidebar with no arrow.")



# Custom CSS for styling
st.markdown(
    """
    <style>
        /* Position the sidebar starting from a specific location */
        .css-1d391kg {
            position: fixed !important;
            top: 100px; /* Adjust this value to control where the sidebar starts */
            left: 0;
            bottom: 0;
            width: 250px; /* Adjust the width as per your requirement */
            z-index: 1000;
        }

        /* Ensure the header wraps around the sidebar */
        .css-1hbfdn5 {
            margin-left: 250px; /* This margin should match the sidebar width */
            padding-top: 100px; /* Adjust this to move the header down if needed */
        }

        /* Optional: Remove background or style the header */
        .css-1hbfdn5 {
            background-color: transparent !important;
            color: #000; /* Black text or any other color */
        }
        
        /* Optional: Style the sidebar's inner content */
        .css-1mcpo5g {
            color: #000;  /* Black text in the sidebar */
        }
    </style>
    """,
    unsafe_allow_html=True
)




import streamlit as st
from pathlib import Path

# Define the relative path to the image
image_path = Path('images/banner-image.jpg')  # Replace with your relative image path

# Display the image as a banner
st.markdown(
    """
    <style>
        .banner-image {
            width: 100%;  /* Makes the banner stretch across the entire width of the page */
            height: 200px;  /* Adjust the height of the banner */
            object-fit: cover;  /* Ensures the image maintains aspect ratio while covering the area */
        }
    </style>
    """, 
    unsafe_allow_html=True
)

# Display the image from the relative path
st.markdown(f'<img class="banner-image" src="{image_path}" />', unsafe_allow_html=True)

# Main content
st.header("Welcome to the App!")
st.write("This is an app with a custom banner image at the top.")



import streamlit as st

# Initialize session state for button clicks
if "approved" not in st.session_state:
    st.session_state.approved = False
if "rejected" not in st.session_state:
    st.session_state.rejected = False

# Function to handle button clicks
def approve():
    st.session_state.approved = True
    st.session_state.rejected = False  # Reset reject state

def reject():
    st.session_state.approved = False  # Reset approve state
    st.session_state.rejected = True

# Button styling
approve_style = "background-color: green; color: white; font-size: 16px; padding: 8px 16px; border-radius: 5px;" if st.session_state.approved else ""
reject_style = "background-color: red; color: white; font-size: 16px; padding: 8px 16px; border-radius: 5px;" if st.session_state.rejected else ""

# Display buttons with styles
col1, col2 = st.columns(2)
with col1:
    if st.button("👍 Approve", on_click=approve, key="approve"):
        st.write("✅ Approved!")

with col2:
    if st.button("👎 Reject", on_click=reject, key="reject"):
        st.write("❌ Rejected!")

# Show styled buttons dynamically
st.markdown(
    f"""
    <style>
        div[data-testid="stButton"] button:nth-of-type(1) {{ {approve_style} }}
        div[data-testid="stButton"] button:nth-of-type(2) {{ {reject_style} }}
    </style>
    """,
    unsafe_allow_html=True
)

