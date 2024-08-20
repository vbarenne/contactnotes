#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 09:53:19 2024

@author: victoriawork
"""

import streamlit as st
import numpy as np
import streamlit as st
import numpy as np
from audio_recorder_streamlit import audio_recorder
from datetime import datetime, timedelta
from models import UploadMethod, CommunicationChannel, ContactType
from helper.prompt_helpers import get_options
from helper.display_helpers import set_stage, add_field, delete_field, display_note, successful_submission_message, button_click
from helper.validate_helpers import get_contact_note_information, check_note_for_missing_information
from helper.session_storage import add_note_to_history, initialize_session_state, save_contact_note_state
import copy
from country_list import countries_for_language

## Page Setup
st.set_page_config(page_title="Validate", page_icon="📈")
st.session_state.is_live_demo = st.sidebar.toggle("Live Demo", value=True)
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
st.markdown("# Validate")
initialize_session_state()


st.markdown("## 1. Upload a voice recording or text file")
upload_method = st.radio(label= "Upload Method", 
                         options= [m.value for m in UploadMethod], 
                         index = 1)

if upload_method == UploadMethod.Manual:
    note = st.text_area("Input your note below", 
                        height = 150,
                        disabled=st.session_state.buttons_click_status[0]
                        )
    st.button('Upload Note', on_click=button_click, args = (1, note), disabled= st.session_state.buttons_click_status[0])
    
elif upload_method == "Joice":
    uploaded_file = st.file_uploader("Choose an audio file to transcribe into contact notes", 
                             accept_multiple_files=False,
                             disabled= st.session_state.buttons_click_status[0])
    
    st.button("Transcribe audio file using Joice", 
              on_click=button_click, 
              args=(0.5,), 
              disabled= st.session_state.buttons_click_status[0])
    
    if uploaded_file and st.session_state.stage > 0: 
        # with open('recording1.txt') as notes:
        #     st.session_state.text = notes.read()
        st.session_state.text = uploaded_file.read().decode("utf-8")
        note = st.text_area("Edit the transcription below to make any corrections necessary:", 
                                   value=st.session_state.text, 
                                   height = 100,
                                   disabled= st.session_state.buttons_click_status[0])
        st.button('Confirm Edits', on_click=button_click, args = (1, note), disabled= st.session_state.buttons_click_status[0])

elif upload_method == "CLM":
    st.write("TBD")



if st.session_state.stage >= 1:
    
    st.markdown("## 2. Edit contact note details")
    st.markdown("Based on the transcription, the following was inferred. Please make any necessary corrections:")
    contact_note, channel_index = get_contact_note_information(note, is_live_demo = st.session_state.is_live_demo)
    col1, col2 = st.columns(2)
    tile1 = st.container(border = True)

    contact_note["communication_channel"] = tile1.selectbox("Communication Channel", 
                                                            get_options(CommunicationChannel),
                                                            index = channel_index,
                                                            disabled = st.session_state.buttons_click_status[1])
    
    
    contact_note["contact_types"]= tile1.multiselect("Contact Type(s)", 
                                                    get_options(ContactType), 
                                                    default= contact_note["contact_types"],
                                                    disabled = st.session_state.buttons_click_status[1])

    cols = tile1.columns(4)
    contact_note["start_date"] = cols[0].date_input(label = "Start of Contact", value = contact_note["start_date"])
    contact_note["start_time"] = cols[1].time_input(label = "Start of Contact", value = contact_note["start_time"], label_visibility= "hidden")
    contact_note["end_date"] = cols[2].date_input(label = "End of Contact", value = contact_note["end_date"])
    contact_note["end_time"] = cols[3].time_input(label = "End of Contact", value = contact_note["end_time"], label_visibility= "hidden")

    contact_note["attendees"] = tile1.text_input("Attendees", 
                                                    value = "; ".join(contact_note["attendees"]),
                                                    disabled = st.session_state.buttons_click_status[1])

    contact_note["attendees"] = [a.strip() for a in contact_note["attendees"].split(";")]

    contact_note["cross_border"] = tile1.radio(label= "Cross-border Activity", 
                            options= ["Yes", "No"], 
                            index = None)
    
    if contact_note["cross_border"] =="Yes":
        contact_note["country"] = tile1.selectbox("Country", options = [country for (iso, country) in dict(countries_for_language('en')).items()])
    else: 
        contact_note["country"] = None 
    st.button('Confirm Details', on_click=button_click, args = (2,), disabled = st.session_state.buttons_click_status[1])
    


if st.session_state.stage >=2:   
    st.markdown("## 3. Validate Contact Notes")
    contact_note["text"] = st.session_state.note_history[-1]["note_content"]
    display_note(contact_note)
    st.markdown(f"""In order to protect the client, the bank and yourself, the five 'W's should be 
                    documented in each contact note.""") 
    if st.session_state.stage<3:             
        questions = check_note_for_missing_information(contact_note, is_live_demo = st.session_state.is_live_demo)
        st.session_state.questions = copy.deepcopy(questions)
        st.session_state.stage = 3
    if len(st.session_state.questions) == 0: 
        check_results = "Based on our analysis, the contact note entered seems to be complete."
        st.write(check_results)
        edited_note = copy.deepcopy(st.session_state.note_history[-1]["note_content"])
    else: 
        check_results = """Based on our analysis, the contact note seems to be missing some information. 
        Please answer the below question to ensure it is compliant. """
        st.write(check_results)
        additional_information = []
        for q in st.session_state.questions:
            additional_information.append(st.text_area(q, height = 100, disabled = st.session_state.buttons_click_status[2]))    
        edited_note =  copy.deepcopy(st.session_state.note_history[-1]["note_content"]) + " " + " ".join(additional_information)
    if st.button('Submit', on_click= button_click, args=(3, edited_note), disabled= st.session_state.buttons_click_status[2]):
        successful_submission_message()        
        save_contact_note_state(contact_note, st.session_state.note_history[-1]["note_content"])

