import openai
import streamlit as st
from openai import AsyncOpenAI

st.title("ChatGPT-like Clone")

# Streamlit secret key handling
openai.api_key = st.secrets["OPENAI_API_KEY"]

client = AsyncOpenAI()


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

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
        response = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        full_response = ""
        for chunk in response:
            chunk_message = chunk['choices'][0]['delta'].get('content', '')
            full_response += chunk_message
            st.markdown(chunk_message)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
