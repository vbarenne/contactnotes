from config import IS_DEMO
from models import CommunicationChannel, ContactType, ContactNote
from helper.openai_model import PromptModel
from datetime import datetime
from helper.prompt_helpers import load_prompt_templ, get_options
import numpy as np
import streamlit as st
import json

# IS_DEMO = True
def get_string_representation_list(list: list) -> str:
    return "[\'" + "\', \'".join(list) + "\']"

def get_contact_note_information(text):      
    if IS_DEMO:        
        note_info = {"date_of_contact": "16.07.2024", 
                    "communication_channel": "In Person",
                    "contact_types": "Recommendation of Investment Products",
                    "attendees": ["Mr. Dubois"]
                    }  
    else: 
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

    channel_index = np.where(np.array(get_options(CommunicationChannel))==note_info["communication_channel"])[0].item()
    note_info["text"] = text
    return note_info, channel_index


def check_note_for_missing_information(text):
    if IS_DEMO: 
        unanswered_questions = ["Where did the meeting with Mr. Dubois take place?", 
                    "What specific socially responsible investment options did you discuss with Mr. Dubois?"]
    else:
        model = PromptModel()
        prompt = load_prompt_templ("prompts/validation_prompt.txt", {"CONTACT_NOTE": text})
        questions_str = model.run_prompt(prompt)
        # Converting string representation of a JSON outputted by the model to an actual JSON
        questions_str = "{" + questions_str.split("{")[1].split("}")[0].replace("\n", "").strip() + "}"
        questions_json = json.loads(questions_str)
        unanswered_questions = [q for (q, v) in questions_json.items() if v == "no"]

    return unanswered_questions

            
     