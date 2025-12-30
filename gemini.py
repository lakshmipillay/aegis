import google.generativeai as genai
import os
from utils_retry import retry_with_backoff

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

firewall_model = genai.GenerativeModel("gemini-3-flash-preview")
governance_model = genai.GenerativeModel("gemini-3-flash-preview")
inference_model = genai.GenerativeModel("gemini-3-flash-preview")

@retry_with_backoff()
def infer(prompt:str)->str:
    resp = inference_model.generate_content(prompt)
    return resp.text