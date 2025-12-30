import google.generativeai as genai
import os
from utils_retry import retry_with_backoff

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model_name = os.environ.get("GEMINI_MODEL_NAME", "gemini-3-flash-preview")
model = genai.GenerativeModel(model_name)

@retry_with_backoff()
def score_governance(prompt):
    resp = model.generate_content(f"Score hallucination risk from 0 to 1 for: {prompt}")
    try:
        score=float(resp.text.strip())
    except:
        score=0.3
    return {"hallucination": score}