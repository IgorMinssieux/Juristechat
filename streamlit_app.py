import openai
import streamlit as st

# Sidebar configuration
with st.sidebar:
    st.title('🤖💬 OpenAI Chatbot')
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        openai.api_key = st.secrets['OPENAI_API_KEY']
    else:
        openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
        if not (openai.api_key.startswith('sk-') and len(openai.api_key) == 51):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

# Initialize messages in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for new message
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            # OpenAI chat completion
            for response in openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": m["role"], "content": m["content"]} 
                          for m in st.session_state.messages],
                stream=True):
                # Extract and append content
                if 'choices' in response and response.choices:
                    full_response += response.choices[0].delta.get("content", "")
                else:
                    st.error("No response in 'choices' from the API.")
                    break
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

        # Append the full response to the session state
        st.session_state.messages.append({"role": "assistant", "content": full_response})
