import chainlit as cl
import random

# ✅ Mock LLM function
def mock_llm_response(query):
    """Simulates an LLM response based on user input."""
    responses = [
        f"That's an interesting question about '{query}', let me think...",
        f"Based on what I know, '{query}' is quite complex, but here's a simple answer.",
        f"You asked about '{query}'. I believe it relates to a broader topic!",
    ]
    return random.choice(responses)

# ✅ Mock autocomplete suggestions
def mock_autocomplete(query):
    """Generates mock autocomplete suggestions."""
    suggestions = [
        f"{query} meaning",
        f"{query} example",
        f"{query} vs other concepts",
        f"How does {query} work?",
        f"Explain {query} simply"
    ]
    return random.sample(suggestions, 3)  # Pick 3 random suggestions

# ✅ Chainlit chat start
@cl.on_chat_start
async def start():
    await cl.Message(content="Welcome! Ask me anything.").send()

# ✅ Chainlit message handler
@cl.on_message
async def main(message):
    """Handles user queries."""
    user_query = message.content

    # Step 1: Generate mock autocomplete suggestions
    suggestions = mock_autocomplete(user_query)
    await cl.Message(content=f"Suggestions: {', '.join(suggestions)}").send()

    # Step 2: Generate mock LLM response
    llm_response = mock_llm_response(user_query)

    # Step 3: Send response to user
    await cl.Message(content=llm_response).send()
