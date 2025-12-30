
import os, time, requests

DD_API_KEY=os.getenv("DD_API_KEY")
DD_APP_KEY=os.getenv("DD_APP_KEY")

def emit_metrics(inp,out,fw,gov):
    ts=int(time.time())
    series=[
        {"metric":"aegis.llm.firewall.blocked","points":[[ts,0 if fw['allowed'] else 1]]},
        {"metric":"aegis.llm.hallucination","points":[[ts,gov.get('hallucination',0.0)]]}
    ]
    requests.post("https://api.datadoghq.com/api/v1/series",
        headers={"DD-API-KEY":DD_API_KEY,"Content-Type":"application/json"},
        json={"series":series})
