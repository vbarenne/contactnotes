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

def get_note_info_as_text(note):
    if note["start_date"] != note["end_date"]: 
        contact_time_span = note["start_date"].strftime("%d.%m.%Y") + " " + note["start_time"].strftime("%H:%M") +  " - " + note["end_date"].strftime("%d.%m.%Y") + " " + note["end_time"].strftime("%H:%M")
    else: 
        contact_time_span = note["start_date"].strftime("%d.%m.%Y") + " " + note["start_time"].strftime("%H:%M") + " - " + note["end_time"].strftime("%H:%M")
    
    country = f" ({note['country']})" if note["country"] is not None else ""

    note_info_string = f"""
    **Contact Time Span:** {contact_time_span}   
    **Communication Channel:** {note["communication_channel"]}  
    **Contact Type(s):** {", ".join(note["contact_types"])}  
    **Attendees:** {", ".join(note["attendees"])}    
    **Cross-border Activity:** {note["cross_border"] + country}   
    **Note:** {note["text"]}
    """
    return note_info_string

def display_note(note):
    note_info_string = get_note_info_as_text(note)
    with st.expander(f"Captured Contact Note", expanded=True): 
        st.markdown(note_info_string)
        
def button_click(button_no, text=""):
    if text!="":
        add_note_to_history(text)
    st.session_state.stage = button_no
    if button_no in range(len(st.session_state.buttons_click_status)):
        st.session_state.buttons_click_status[button_no-1] = True

 