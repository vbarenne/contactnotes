#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 09:53:19 2024

@author: victoriawork
"""

import streamlit as st
import numpy as np
from helper.display_helpers import display_note, get_note_info_as_text
import copy
from helper.prompt_helpers import load_prompt_templ
from helper.openai_model import PromptModel
import json
import ast

st.set_page_config(page_title="Action Items & Minutes", page_icon="📈")
st.markdown("# Action Items & Meeting Minutes")
note_info = copy.deepcopy(st.session_state.validated_note)

display_note(note_info)

def get_summary_action_minutes(note_info, is_live_demo = False):
    if note_info["start_date"] != note_info["end_date"]: 
        contact_time_span = note_info["start_date"].strftime("%d.%m.%Y") + " " + note_info["start_time"].strftime("%H:%M") +  " - " + note_info["end_date"].strftime("%d.%m.%Y") + " " + note_info["end_time"].strftime("%H:%M")
    else: 
        contact_time_span = note_info["start_date"].strftime("%d.%m.%Y") + " " + note_info["start_time"].strftime("%H:%M") + " - " + note_info["end_time"].strftime("%H:%M")

    if is_live_demo: 
        model = PromptModel()
        prompt = load_prompt_templ("prompts/summary_action_minutes_prompt.txt", {"CONTACT_NOTE_TEXT": get_note_info_as_text(note_info)})

        model_response = model.run_prompt(prompt)
        model_response = "{" + model_response.split("{")[1].split("}")[0].replace("\n", "").strip() + "}"
        model_response_json = json.loads(model_response)
        summary, action_items, meeting_minutes = [v for (k,v) in model_response_json.items()]
    else:
        summary = load_prompt_templ("demo_dummies/summary_dummy.txt", {})
        action_items = load_prompt_templ("demo_dummies/action_items_dummy.txt", {})
        action_items = ast.literal_eval(action_items)
        meeting_minutes = load_prompt_templ("demo_dummies/meeting_minutes_dummy.txt", {})
    return summary, action_items, meeting_minutes 

summary, action_items, meeting_minutes = get_summary_action_minutes(note_info, is_live_demo= st.session_state.is_live_demo)

st.markdown("**Summary**")
st.markdown(summary) 
st.markdown("**Action Items**")
for item in action_items:
    st.markdown("* " + item)

if st.button("Generate Meeting Minutes"):
    with st.expander(f"Generated Meeting Minutes", expanded=True): 
        st.markdown(meeting_minutes) 



