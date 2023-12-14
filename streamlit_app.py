import os
import streamlit as st
from openai import OpenAI
# Set your OpenAI API key

with st.sidebar:
    st.title('🤖💬 OpenAI Chatbot')
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        client = OpenAI(
            api_key=os.environ['OPENAI_API_KEY'],
        )
        
    else:
        openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
        if not (openai.api_key.startswith('sk-') and len(openai.api_key) == 51):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            response = client.completions.create(model='curie')
            full_response += response.choices[0].text.strip()
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    st.session_state.messages.append({"role": "assistant", "content": full_response})
