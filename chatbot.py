import chainlit as cl
import google.generativeai as genai

# ✅ Configure Gemini Model
genai.configure(api_key="YOUR_GEMINI_API_KEY")  # Replace with a secure API key

# ✅ Fixed Autocomplete Function
def autocomplete_query(partial_query):
    """Generate autocomplete suggestions using Gemini."""
    model = genai.GenerativeModel("gemini-1.5-flash")  # Fast model for autocomplete
    response = model.generate_content(f"Suggest 5 autocomplete completions for: {partial_query}")
    return response.text.split("\n")  # Convert output to a list of suggestions

# ✅ Fixed Response Generation
def generate_response(query):
    """Generate response using Gemini."""
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Answer the question: {query}"
    response = model.generate_content(prompt)
    return response.text

# ✅ Chainlit Chat Start (Fixes missing callback issue)
@cl.on_chat_start
async def start():
    await cl.Message(content="Welcome! Type your question to start.").send()

@cl.on_message
async def main(message):
    """Handles user queries in Chainlit."""
    user_query = message.content

    # Step 1: Get autocomplete suggestions
    suggestions = autocomplete_query(user_query)
    await cl.Message(content=f"Suggestions: {', '.join(suggestions)}").send()

    # Step 2: Generate response with Gemini
    final_response = generate_response(user_query)

    # Step 3: Send response to user
    await cl.Message(content=final_response).send()
