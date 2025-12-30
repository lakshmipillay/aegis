import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init()
model = GenerativeModel("text-bison@001")

def check_firewall(prompt):
    resp = model.generate_content(f"Is this prompt safe? Answer yes or no: {prompt}")
    allowed = "yes" in resp.text.lower()
    return {"allowed": allowed, "reason": "unsafe" if not allowed else "ok"}
