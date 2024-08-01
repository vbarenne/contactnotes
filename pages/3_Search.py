#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 09:53:19 2024

@author: victoriawork
"""

import streamlit as st
from config import IS_DEMO

st.set_page_config(page_title="Search", page_icon="📈")
st.markdown("# Search")


# st.caption("🚀 A Streamlit chatbot powered by OpenAI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    if IS_DEMO: 
        if prompt.startswith("Who"):
            msg = "It was mentioned previously that Mr. Dubois has a grandson."   
        else: 
            msg = f"""
            You can find this information in the contact note recorded 
            on 17.07.2024: 'He's excited about his grandson's 
            upcoming wedding'
            """
            
    
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)