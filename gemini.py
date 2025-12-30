
import vertexai
from vertexai.generative_models import GenerativeModel
import os



def infer(prompt:str)->str:
    model_name = os.environ.get("GEMINI_MODEL_NAME", "gemini-3-flash-preview")
    inference_model = GenerativeModel(model_name)
    resp = inference_model.generate_content(prompt)
    return resp.text
