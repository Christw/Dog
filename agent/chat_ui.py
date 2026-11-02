
import streamlit as st
from agent.assistant import get_answer

def render_chat_page():

    st.title("🐶 Dog AI Assistant")
    st.write("Ask me anything about dogs!")

    if "dog_chat_history" not in st.session_state:
        st.session_state.dog_chat_history = []

    for message in st.session_state.dog_chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask a question about dogs...")

    if prompt:
        st.session_state.dog_chat_history.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer = get_answer(
                        st.session_state.dog_chat_history[-10:]
                    )
                    st.markdown(answer)

                    st.session_state.dog_chat_history.append({
                        "role": "assistant",
                        "content": answer
                    })

                except Exception:
                    st.error(
                        "Sorry, something went wrong. "
                        "Please check your API configuration."
                    )
