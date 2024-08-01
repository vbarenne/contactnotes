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
from datetime import datetime
from models import UploadMethod, CommunicationChannel, ContactType
from helper.prompt_helpers import get_options
from helper.display_helpers import set_stage, add_field, delete_field, display_note, successful_submission_message, button_click
from helper.validate_helpers import get_contact_note_information, check_note_for_missing_information
from helper.session_storage import add_note_to_history, initialize_session_state, save_contact_note_state
import copy

## Page Setup
st.set_page_config(page_title="Validate", page_icon="📈")
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
    
# elif upload_method == "Joice":
#     note = st.file_uploader("Choose an audio file to transcribe into contact notes", 
#                              accept_multiple_files=False)
    
#     st.button("Transcribe audio file using Joice", on_click=set_stage, args=(0.5,))
    
#     if note and st.session_state.stage > 0: 
#         with open('recording1.txt') as notes:
#             st.session_state.text = notes.read()
#         note = st.text_area("Edit the transcription below to make any corrections necessary:", 
#                                    value=st.session_state.text, 
#                                    height = 100)
#         st.button('Confirm Edits', on_click=add_session_note_history)

# elif upload_method == "CLM":
#     st.write("TBD")



if st.session_state.stage >= 1:

    st.markdown("## 2. Edit contact note details")
    st.markdown("Based on the transcription, the following was inferred. Please make any necessary corrections:")
    contact_note, channel_index = get_contact_note_information(note)
    col1, col2 = st.columns(2)

    with col1: 
        tile1 = col1.container(border = True)
        if contact_note["communication_channel"] in get_options(CommunicationChannel): 
            contact_note["communication_channel"] = tile1.selectbox("Communication Channel", 
                                                                    get_options(CommunicationChannel),
                                                                    index = channel_index,
                                                                    disabled = st.session_state.buttons_click_status[1])
        if np.isin(np.array(contact_note["contact_types"]), np.array(get_options(ContactType))).all():
            contact_note["contact_types"]= tile1.multiselect("Contact Type(s)", 
                                                            get_options(ContactType), 
                                                            default= contact_note["contact_types"],
                                                            disabled = st.session_state.buttons_click_status[1])
        if contact_note["date_of_contact"] !="unknown": 
            contact_note["date_of_contact"] = tile1.date_input("Date of Contact", 
                                                            value = datetime.strptime(contact_note["date_of_contact"], "%d.%m.%Y"),
                                                            disabled = st.session_state.buttons_click_status[1])
    

    with col2: 
        tile2 = col2.container(border = True)
        if "fields_size" not in st.session_state:
            st.session_state.fields_size = len(contact_note["attendees"])
            st.session_state.fields = contact_note["attendees"]
            st.session_state.deletes = []
        
        c1, c2 = tile2.columns(2)
        # fields and types of the table
        for i in range(st.session_state.fields_size):
            value = contact_note["attendees"][i] if len(contact_note["attendees"]) > i else None
            with c1:
                st.session_state.fields.append(st.text_input(f"Attendee {i +1}", 
                                                             value = value,
                                                             disabled = st.session_state.buttons_click_status[1]))
            with c2:
                st.session_state.deletes.append(st.button("X", 
                                                          key=f"delete{i +1}", 
                                                          on_click=delete_field, args=(i,),
                                                          disabled = st.session_state.buttons_click_status[1]
                                                          ))
        tile2.button("+ Add Attendee", on_click=add_field, disabled = st.session_state.buttons_click_status[1])

    st.button('Confirm Details', on_click=button_click, args = (2,), disabled = st.session_state.buttons_click_status[1])
    
if st.session_state.stage >=2:
    st.markdown("## 3. Validate Contact Notes")
    display_note(contact_note)
    st.markdown(f"""In order to protect the client, the bank and yourself, the five 'W's should be 
                    documented in each contact note.""")              
    questions = check_note_for_missing_information(contact_note["text"])

    if len(questions) == 0: 
        check_results = "Based on our analysis, the contact note entered seems to be complete."
    else: 
        check_results = """Based on our analysis, the contact note seems to be missing some information. 
        Please answer the below question to ensure it is compliant. """

        additional_information = []
        for q in questions:
            additional_information.append(st.text_area(q, height = 100, disabled = st.session_state.buttons_click_status[2]))    

    edited_note =  copy.deepcopy(st.session_state.note_history[-1]["note_content"]) + " " + " ".join(additional_information)
    if st.button('Submit', on_click= button_click, args=(3, edited_note), disabled= st.session_state.buttons_click_status[2]):
        successful_submission_message()        
        save_contact_note_state(contact_note, st.session_state.note_history[-1]["note_content"])
