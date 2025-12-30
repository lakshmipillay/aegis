import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init()
model = GenerativeModel("text-bison@001")

def score_governance(prompt):
    resp = model.generate_content(f"Score hallucination risk from 0 to 1 for: {prompt}")
    try:
        score = float(resp.text.strip())
    except:
        score = 0.3
    return {"hallucination": score}
