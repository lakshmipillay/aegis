import os, time, requests

DD_API_KEY = os.getenv("DD_API_KEY")
DD_APP_KEY = os.getenv("DD_APP_KEY")
SITE = "https://api.datadoghq.com"

def emit_metrics(prompt, output, fw, gov, error=False):
    ts = int(time.time())

    tokens_in = len(prompt.split())
    tokens_out = len(output.split())
    cost = (tokens_in + tokens_out) * 0.000002  # mock $/token for demo

    series = [
        {"metric": "aegis.llm.requests", "points": [[ts, 1]], "type": "count"},
        {"metric": "aegis.llm.errors", "points": [[ts, 1 if error else 0]], "type": "count"},
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

    r = requests.post(
      "https://llmobs.datadoghq.com/api/v2/llm/traces",
      headers={
        "DD-API-KEY": DD_API_KEY,
        "DD-APPLICATION-KEY": DD_APP_KEY,
        "Content-Type": "application/json"
      },
      json={
        "data": [
            {
                "type": "llm_trace",
                "attributes": {
                    "ml_app": "aegis",
                    "model": "gemini",
                    "provider": "google",
                    "service": "aegis",
                    "env": "prod",
                    "prompt": {
                        "messages": [
                            { "role": "user", "content": prompt }
                        ]
                    },
                    "response": {
                        "messages": [
                            { "role": "assistant", "content": output }
                        ]
                    },
                    "metrics": {
                        "tokens_in": tokens_in,
                        "tokens_out": tokens_out,
                        "hallucination": gov.get("hallucination", 0),
                        "blocked": not fw["allowed"]
                    }
                }
            }
        ]
    },
    timeout=3
)

    print("LLM TRACE:", r.status_code, r.text)
