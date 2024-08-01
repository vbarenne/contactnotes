from decouple import config
import os

# OpenAI
OPENAI_API_KEY = config("OPENAI_API_KEY",  os.getenv('OPENAI_API_KEYf'))
OPENAI_SERVICE = config("OPENAI_SERVICE", "")
PROMPT_MODEL = "gpt-4o"

# If set to true, will retreive dummy demo data instead of calling OpenAI model
IS_DEMO = config("IS_DEMO", True)
