import streamlit as st
from groq import Groq

# Initialize Groq client with your API key
client = Groq(api_key="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")

# Set up Streamlit page
st.set_page_config(page_title="Cybersecurity Assistant", page_icon="🛡")
st.title("🛡 Cybersecurity Assistant")
st.write(
    "Welcome to your personal cybersecurity assistant. "
    "Ask me about anything from protecting your device, identifying threats, choosing the right tools, or understanding the latest in cybersecurity."
)

# Session state to store conversation
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are a knowledgeable and helpful cybersecurity expert. Provide clear, concise, and accurate answers related to cybersecurity topics. "
            "Offer advice on protecting personal and organizational systems, identifying vulnerabilities, using security tools, and understanding threats like phishing, malware, and ransomware. "
            "Use non-technical explanations when the user seems unfamiliar with the topic. If needed, ask clarifying questions. "
            "Be friendly, professional, and prioritize user security."
        )}
    ]

# User input
user_input = st.chat_input("What would you like to know about cybersecurity?")

# Display conversation history
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Process new input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        # Call Groq API with conversation
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=1000,
            stream=True,
        )

        # Stream the assistant's response
        full_reply = ""
        response_container = st.empty()
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                full_reply += content
                response_container.markdown(full_reply)

        # Save assistant's reply to session state
        st.session_state.messages.append({"role": "assistant", "content": full_reply})