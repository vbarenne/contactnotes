from decouple import config
import os
import streamlit as st

# OpenAI
OPENAI_API_KEY = config("OPENAI_API_KEY",  st.secrets["OPENAI_API_KEY"])
OPENAI_SERVICE = config("OPENAI_SERVICE", "")
PROMPT_MODEL = "gpt-4o"
