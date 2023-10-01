import openai
import streamlit as st

st.title("OpenAI - ChatGPT")

openai.api_type =  st.secrets["OPENAI_API_TYPE"]
openai.api_version = st.secrets["OPENAI_API_VERSION"]
openai.api_base = st.secrets["OPENAI_API_BASE"]
openai.api_key = st.secrets["OPENAI_API_KEY"]


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = st.secrets["OPENAI_MODEL"]

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
        for response in openai.ChatCompletion.create(
            engine=st.secrets["OPENAI_MODEL"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})