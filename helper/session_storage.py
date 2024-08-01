import json
from typing import List
import streamlit as st
from datetime import datetime
from models import ContactNote


def initialize_session_state():
    if "stage" not in st.session_state:
        st.session_state.stage = 0
    if "note_history" not in st.session_state:
        st.session_state.note_history = []
    if "buttons_click_status" not in st.session_state:
        st.session_state.buttons_click_status = [False, False, False]


def add_note_to_history(text):
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    if len(st.session_state.note_history)==0:
        st.session_state.note_history.append({"timestamp": timestamp, "note_content": text})
    elif st.session_state.note_history[-1]["note_content"]!= text: 
        st.session_state.note_history.append({"timestamp": timestamp, "note_content": text})


def save_contact_note_state(contact_note, note_content_overwrite: str = ""):
    if note_content_overwrite != "":
        contact_note["text"] = note_content_overwrite
    st.session_state.validated_note = contact_note