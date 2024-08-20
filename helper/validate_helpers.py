from models import CommunicationChannel, ContactType, ContactNote
from helper.openai_model import PromptModel
from datetime import datetime
from helper.prompt_helpers import load_prompt_templ, get_options
from helper.display_helpers import get_note_info_as_text
import numpy as np
import streamlit as st
import json

def get_string_representation_list(list: list) -> str:
    return "[\'" + "\', \'".join(list) + "\']"

def get_contact_note_information(text, is_live_demo = False):      
    if is_live_demo: 
        model = PromptModel()
        prompt = load_prompt_templ("prompts/prefill_fields_prompt.txt", {"TODAY_DATE": datetime.now().strftime("%d.%m.%Y"),
                                                                         "COMMUNICATION_CHANNEL_OPTIONS": get_string_representation_list(get_options(CommunicationChannel)),
                                                                         "CONTACT_TYPE_OPTIONS": get_string_representation_list(get_options(ContactType)),
                                                                         "CONTACT_NOTE": text})
        note_info_str = model.run_prompt(prompt)
        # Converting string representation of a JSON outputted by the model to an actual JSON
        note_info_str = "{" + note_info_str.split("{")[1].split("}")[0].replace("\n", "").strip() + "}"
        note_info = json.loads(note_info_str)
        note_info["contact_types"] = [c.strip() for c in note_info["contact_types"].split(",")]
        note_info["attendees"] = [attendee.strip() for attendee in note_info["attendees"].split(",")]
    else: 
        note_info = {"start_date": "16.07.2024", 
                     "end_date": "16.07.2024", 
                     "start_time": "14:00",
                     "end_time": "15:30",
            "communication_channel": "In Person",
            "contact_types": ["Recommendation of Investment Products"],
            "attendees": ["Mr. Dubois"]
            }  
    
    if note_info["communication_channel"] in get_options(CommunicationChannel):
        channel_index = np.where(np.array(get_options(CommunicationChannel))==note_info["communication_channel"])[0].item()
    else: 
        channel_index = None

    for key in note_info:
        if note_info[key]== "unknown" or (isinstance(note_info[key], list) and "unknown" in note_info[key]):
            note_info[key] = None
        if key in ["start_date", "end_date"] and note_info[key] is not None: 
            note_info[key] = datetime.strptime(note_info[key], "%d.%m.%Y")
        elif key in ["start_time", "end_time"] and note_info[key] is not None:
            note_info[key] = datetime.strptime(note_info[key], "%H:%M")
    return note_info, channel_index


def check_note_for_missing_information(note_info, is_live_demo = False):
    if is_live_demo:
        model = PromptModel()
        prompt = load_prompt_templ("prompts/validation_prompt.txt", {"CONTACT_NOTE_TEXT": get_note_info_as_text(note_info)})
        questions_str = model.run_prompt(prompt)
        # Converting string representation of a JSON outputted by the model to an actual JSON
        questions_str = "{" + questions_str.split("{")[1].split("}")[0].replace("\n", "").strip() + "}"
        questions_json = json.loads(questions_str)
        unanswered_questions = [q for (q, v) in questions_json.items() if v == "no"]
    else: 
        unanswered_questions = ["Where did the meeting with Mr. Dubois take place?", 
                "What specific socially responsible investment options did you discuss with Mr. Dubois?"]
    return unanswered_questions

            
     