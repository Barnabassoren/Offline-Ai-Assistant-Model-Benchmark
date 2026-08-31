import streamlit as st
import sys
import os

# src folder ko path mein add karo, taaki import kaam kare
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from main import ask_question

st.title("Offline AI Assistant")
st.write("Apne college notes se sawaal poocho!")

#if chat history doesn't present in session then start with empty list
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "input_key" not in st.session_state:
    st.session_state.input_key = 0

user_query = st.text_input("Type your Question:", key=f"input_{st.session_state.input_key}")

if st.button("Ask me!"):
    if user_query:
        with st.spinner("Thinking..."):
            outcome = ask_question(user_query)

        if outcome["result"]:
            st.session_state.chat_history.append({
                "question": user_query,
                "answer": outcome["result"].answer,
                "confidence": outcome["result"].confidence
            })
            st.session_state.input_key += 1  #new input box
            st.rerun()                        #refresh immediately 
        else:
            st.error("failed to find the result")
    else:
        st.warning("Ask me first any question!")
#show whole history
st.write("---")
for chat in reversed(st.session_state.chat_history):
    st.write(f"**Q:** {chat['question']}")
    st.write(f"**A:** {chat['answer']}")
    st.write(f"*Confidence: {chat['confidence']}*")
    st.write("---")