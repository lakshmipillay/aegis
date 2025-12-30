import vertexai
from vertexai.generative_models import GenerativeModel
import os




def score_governance(prompt):
    model_name = os.environ.get("GEMINI_MODEL_NAME", "gemini-3-flash-preview")
    model = GenerativeModel(model_name)

    resp = model.generate_content(f"Score hallucination risk from 0 to 1 for: {prompt}")
    try:
        score = float(resp.text.strip())
    except:
        score = 0.3
    return {"hallucination": score}
