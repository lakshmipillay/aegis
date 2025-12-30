
from fastapi import FastAPI, Body
from firewall import check_firewall
from governance import score_governance
from gemini import infer
from telemetry import emit_metrics

app = FastAPI()

@app.post("/infer")
def infer_endpoint(prompt: str = Body(..., embed=True)):
    try:
        fw = check_firewall(prompt)
        if not fw["allowed"]:
            emit_metrics(prompt, "", fw, {"hallucination":0.0}, error=False)
            return {"blocked": True, "reason": fw["reason"]}

        gov = score_governance(prompt)
        output = infer(prompt)

        emit_metrics(prompt, output, fw, gov, error=False)
        return {"output": output, "governance": gov}

    except Exception as e:
        emit_metrics(prompt, "", {"allowed": True}, {"hallucination":0.0}, error=True)
        raise
