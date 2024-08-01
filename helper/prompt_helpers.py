from enum import Enum
import re

def get_options(enum_class: Enum):
    return [member.value for member in enum_class]


def load_prompt_templ(file_path: str, replace_dict: dict) -> str:
    """
    Loads a prompt template from a file and replaces the placeholders with the values from the replacement dictionary, which includes the value to replace as its key and the replacement value as its value.
    Placeholders should start and end with %% (i.e. %%PLACEHOLDER%%).

    Args:
        file_path (str): The path to the file containing the prompt template.
        replace_dict (dict): The dictionary containing the replacement values.
    Returns:
        str: The prompt template with the placeholders replaced with the values from the replacement dictionary.
    """
    with open(file_path, "r") as f:
        text = f.read()
        replacements = re.findall(r"%%(.*)%%", text)
        for replacement in replacements:
            text = text.replace(f"%%{replacement}%%", replace_dict.get(replacement, ""))
        return text