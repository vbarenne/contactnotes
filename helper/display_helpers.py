import streamlit as st
from helper.session_storage import add_note_to_history
import copy

def set_stage(stage):
    st.session_state.stage = stage

def add_field():
    st.session_state.fields_size += 1

def delete_field(index):
    st.session_state.fields_size -= 1
    del st.session_state.fields[index]
    del st.session_state.deletes[index]

def successful_submission_message():
    st.markdown(':gray[*Contact Note Successfully Submitted*]')

def display_note(note):
    with st.expander(f"Captured Contact Note", expanded=True): 
        st.markdown(f"""
                  **Date of the contact:** {note["date_of_contact"]}  
                  **Communication Channel:** {note["communication_channel"]}  
                  **Contact Type(s):** {", ".join(note["contact_types"])}  
                  **Attendees:** {", ".join(note["attendees"])}  
                  **Note:** {note["text"]}
                  """)
        
def button_click(button_no, text=""):
    if text!="":
        add_note_to_history(text)
    st.session_state.stage = button_no
    if button_no in range(len(st.session_state.buttons_click_status)):
        st.session_state.buttons_click_status[button_no-1] = True

 