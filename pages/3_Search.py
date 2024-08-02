#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 09:53:19 2024

@author: victoriawork
"""


import streamlit as st
from helper.openai_model import PromptModel
from openai import OpenAI
from config import PROMPT_MODEL
import copy
from helper.prompt_helpers import load_prompt_templ

st.set_page_config(page_title="Search", page_icon="📈")
st.markdown("# Search")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Get the inputted note to give as context to the chatbot
note_info = copy.deepcopy(st.session_state.validated_note)
contact_note_context = load_prompt_templ("prompts/chatbot_context.txt", 
                            {"CONTACT_NOTE": note_info["text"],
                            "DATE_OF_CONTACT": note_info["date_of_contact"].strftime("%d.%m.%Y"),
                            "COMMUNICATION_CHANNEL": note_info["communication_channel"],
                            "CONTACT_TYPES": "; ".join(note_info["contact_types"]),
                            "ATTENDEES": "; ".join(note_info["attendees"])})

# st.caption("🚀 A Streamlit chatbot powered by OpenAI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if st.session_state.is_live_demo: 
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=PROMPT_MODEL,
                    messages=[
                        {"role": m["role"], "content": contact_note_context + m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

    else: 
        if prompt.startswith("Who"):
            msg = "It was mentioned previously that Mr. Dubois has a grandson."   
        else: 
            msg = f"""
            You can find this information in the contact note recorded 
            on {note_info["date_of_contact"].strftime("%d.%m.%Y")}4: 'He's excited about his grandson's 
            upcoming wedding'
            """

        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

