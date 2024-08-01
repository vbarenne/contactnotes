#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 09:53:19 2024

@author: victoriawork
"""

import streamlit as st
import numpy as np
from helper.display_helpers import display_note
import copy
from config import IS_DEMO
from helper.prompt_helpers import load_prompt_templ
from helper.openai_model import PromptModel
import json

st.set_page_config(page_title="Action Items & Minutes", page_icon="📈")
st.markdown("# Action Items & Meeting Minutes")

note_info = copy.deepcopy(st.session_state.validated_note)
display_note(note_info)

def get_summary_action_minutes(note_info):
    if IS_DEMO: 
        summary = load_prompt_templ("demo_dummies/summary_dummy.txt", {})
        action_items = load_prompt_templ("demo_dummies/action_items_dummy.txt", {})
        meeting_minutes = load_prompt_templ("demo_dummies/meeting_minutes_dummy.txt", {})
    else: 
        model = PromptModel()
        prompt = load_prompt_templ("prompts/summary_action_minutes_prompt.txt", {"CONTACT_NOTE": note_info["text"]})
        questions_str = model.run_prompt(prompt)
        # Converting string representation of a JSON outputted by the model to an actual JSON
        questions_str = "{" + questions_str.split("{")[1].split("}")[0].replace("\n", "").strip() + "}"
        questions_json = json.loads(questions_str)
        unanswered_questions = [q for (q, v) in questions_json.items() if v == "no"]
    return summary, action_items, meeting_minutes 

summary, action_items, meeting_minutes = get_summary_action_minutes(note_info)

st.markdown("**Summary**")
st.markdown(summary) 
st.markdown("**Action Items**")
st.markdown(action_items) 

if st.button("Generate Meeting Minutes"):
    with st.expander(f"Generated Meeting Minutes", expanded=True): 
        st.markdown(meeting_minutes) 



