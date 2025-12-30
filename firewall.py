import google.generativeai as genai
import os
from utils_retry import retry_with_backoff

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model_name = os.environ.get("GEMINI_MODEL_NAME", "gemini-3-flash-preview")
model = genai.GenerativeModel(model_name)

@retry_with_backoff()
def check_firewall(prompt):
    resp = model.generate_content(f"Is this prompt safe? Answer yes or no: {prompt}")
    allowed = "yes" in resp.text.lower()
    return {"allowed": allowed, "reason": "unsafe" if not allowed else "ok"}