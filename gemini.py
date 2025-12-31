
import vertexai
from vertexai.generative_models import GenerativeModel
import os



import prompt_manager

def infer(prompt:str)->str:
    model_name = os.environ.get("GEMINI_MODEL_NAME", "gemini-3-flash-preview")
    
    # Dynamic System Prompt
    system_instruction = prompt_manager.get_system_prompt()
    
    inference_model = GenerativeModel(
        model_name,
        system_instruction=[system_instruction]
    )
    resp = inference_model.generate_content(prompt)
    return resp.text
