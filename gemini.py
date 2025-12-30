
import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init()

firewall_model = GenerativeModel("text-bison@001")
governance_model = GenerativeModel("text-bison@001")
inference_model = GenerativeModel("text-bison@001")

def infer(prompt:str)->str:
    resp = inference_model.generate_content(prompt)
    return resp.text
