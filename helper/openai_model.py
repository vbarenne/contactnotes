from config import OPENAI_API_KEY, PROMPT_MODEL
from openai import OpenAI


class PromptModel():
    def _init_model(self):
        return OpenAI(api_key=OPENAI_API_KEY)

    def run_prompt(self, prompt, context: list = []): 
        model = self._init_model()
        prediction_parts = [prompt, *context]
        
        response = model.chat.completions.create(
            model=PROMPT_MODEL,
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": text} for text in prediction_parts
                ]}
            ],
            temperature=0.0,
        )
        return response.choices[0].message.content
    
