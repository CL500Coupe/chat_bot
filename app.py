import openai
import streamlit as st
import asyncio

st.title("ChatGPT-like Clone")

# Streamlit secret key handling
openai.api_key = st.secrets["OPENAI_API_KEY"]

client = openai

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

async def get_response():
    prompt = st.session_state.messages[-1]["content"]
    response = await client.ChatCompletion.acreate(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
    )
    return response.choices[0].message["content"]

def main():
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(get_response())
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
