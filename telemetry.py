import os, time, requests

DD_API_KEY = os.getenv("DD_API_KEY")
DD_APP_KEY = os.getenv("DD_APP_KEY")
SITE = "https://api.datadoghq.com"

def emit_metrics(prompt, output, fw, gov):
    ts = int(time.time())

    tokens_in = len(prompt.split())
    tokens_out = len(output.split())
    cost = (tokens_in + tokens_out) * 0.000002  # mock $/token for demo

    series = [
        {"metric": "aegis.llm.requests", "points": [[ts, 1]]},
        {"metric": "aegis.llm.firewall.blocked", "points": [[ts, 1 if not fw["allowed"] else 0]], "type": "count"},
        {"metric": "aegis.llm.hallucination", "points": [[ts, gov.get("hallucination", 0.0)]]},
        {"metric": "aegis.llm.tokens_in", "points": [[ts, tokens_in]]},
        {"metric": "aegis.llm.tokens_out", "points": [[ts, tokens_out]]},
        {"metric": "aegis.llm.cost_usd", "points": [[ts, cost]]},
    ]

    requests.post(
        f"{SITE}/api/v1/series",
        headers={
            "DD-API-KEY": DD_API_KEY,
            "Content-Type": "application/json",
        },
        json={"series": series},
        timeout=3,
    )
