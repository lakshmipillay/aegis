import vertexai
from vertexai.generative_models import GenerativeModel
import os




def check_firewall(prompt):
    model_name = os.environ.get("GEMINI_MODEL_NAME", "gemini-3-flash-preview")
    model = GenerativeModel(model_name)
    
    resp = model.generate_content(f"Is this prompt safe? Answer yes or no: {prompt}")
    allowed = "yes" in resp.text.lower()
    return {"allowed": allowed, "reason": "unsafe" if not allowed else "ok"}
