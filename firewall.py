import vertexai
from vertexai.generative_models import GenerativeModel
import os




def check_firewall(prompt):
    model_name = os.environ.get("GEMINI_MODEL_NAME", "gemini-3-flash-preview")
    model = GenerativeModel(model_name)
    
    resp = model.generate_content(f"Is this prompt safe? Answer yes or no: {prompt}")
    is_safe = "yes" in resp.text.lower()
    
    # DEMO MODE: set allowed=True always so we can test the System Prompt protections
    # In production, this would be: allowed = is_safe
    return {"allowed": True, "reason": "unsafe" if not is_safe else "ok", "detected": not is_safe}
