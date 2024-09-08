import os
import openai
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv

# load_dotenv(".env")



import streamlit as st
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

pt = """
Introduction: Hi there! I'm here to help with any questions you have. What's on your mind today?

Part 1: Exploring Business Interests

User Prompt: Feel free to share any thoughts or questions you have about businesses, whether you're just curious or thinking about starting one. 
Bot Response: Provides a supportive and relaxed conversation, offers general advice, and encourages the user to share more if they feel comfortable, without pushing for specifics. 

Part 2: Answering Business Questions
User Prompt: If you have any specific questions about business, ask away! I'm here to help. 
Bot Response: Offers tailored advice with practical examples and keeps the conversation light and informative, ensuring the user feels supported. 

Part 3: General Discussion on Business Finances
Try to understand how the user is planning on the finances.
Use subtle prompts to encourage the user to think about additional funding, 
highlight the benefits of financial security, and gently introduce the idea of taking a well-timed loan.

User Prompt: If you're curious about business finances or funding, I can share some insights. What would you like to know? Bot Strategy: Discusses various aspects of business finances in a friendly manner, introduces concepts like budgeting and funding options without assuming the user's intent to start a business. Part 4: Introducing the Aspire App
Bot Pitch: If managing business finances sounds daunting, the Aspire App can help simplify the process. It's easy to use and can assist with applying for loans and managing your business finances. Feel free to download it from 'www.letsaspire.in' . Conclusion: Thank you for chatting with me today! If you have any more questions or just want to talk more about your interests, feel free to reach out through our app or website. We're here to support you, whatever your goals may be!

Chatbot Interaction Guardrails:
Focus: Allow the user to guide the conversation, responding naturally to their queries. Brevity: Encourage concise responses to keep the conversation flowing smoothly. Scope: Maintain focus on business-related topics, but allow for a relaxed approach without pushing the user towards any specific actions. Support: Provide a supportive and friendly tone throughout, catering to users who may not be proficient in English or fully decided on starting a business.
Important: Keep the bot answers short and crisp and do not stretch the conversation too much but not at the cost of it being a natural 
conversation. Naturally go into the decided flow when you feel like it being a good time to bring in costs.
Goal: Naturally make the users download the app.
Important: If the user is interested in a loan, start hard selling the aspire app.
"""


def generate_response(prompt):
    # Prepare the conversation history
    conversation_history = [{"role": "system", "content": pt}]
    conversation_history.extend(st.session_state['messages'])
    conversation_history.append({"role": "user", "content": prompt})

    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=1.2,
    )
    return chat_completion.choices[0].message.content

# Creating the chatbot interface
st.title("Aspire Bot")

# Initialize session state for storing chat history
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Add a greeting message if chat history is empty
if not st.session_state['messages']:
    st.session_state['messages'].append({"role": "assistant", "content": """Hi there! I'm here to help with any 
                                         questions you have. What's on your mind today?"""})

# Display chat history
for message in st.session_state['messages']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("Ask me anything about loans..."):
    # Add user message to chat history
    st.session_state['messages'].append({"role": "user", "content": prompt})

    # Generate response from the model
    response = generate_response(prompt)

    # Add assistant response to chat history
    st.session_state['messages'].append({"role": "assistant", "content": response})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Display the latest assistant message
    with st.chat_message("assistant"):
        st.markdown(response)

