import google.generativeai as genai
import os
from utils_retry import retry_with_backoff

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model_name = os.environ.get("GEMINI_MODEL_NAME", "gemini-3-flash-preview")
firewall_model = genai.GenerativeModel(model_name)
governance_model = genai.GenerativeModel(model_name)
inference_model = genai.GenerativeModel(model_name)

@retry_with_backoff()
def infer(prompt:str)->str:
    resp = inference_model.generate_content(prompt)
    return resp.text