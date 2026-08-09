#the main UI

import os
import sys
import streamlit as st

#add src directory to python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "src"))

from orchestrator import route_query

#page layout setup
st.set_page_config(page_title="Healthcare Assistant", page_icon="🏥", layout="centered")

st.title("Healthcare RAG & SQL Assistant")
st.write("Ask about patient records (SQL) or hospital policy documents (RAG).")

#initialize chat message history
if "messages" not in st.session_state:
    st.session_state.messages = []

#display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

#process user question input
if user_input := st.chat_input("Type your question here..."):
    #append user message to UI
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    #generate response using orchestrator
    with st.chat_message("assistant"):
        with st.spinner("Processing query..."):
            response = route_query(user_input)
            st.write(response)

    #append assistant response to UI
    st.session_state.messages.append({"role": "assistant", "content": response})