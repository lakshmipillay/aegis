import os, time, requests
from ddtrace.llmobs import LLMObs

DD_API_KEY = os.getenv("DD_API_KEY")
DD_APP_KEY = os.getenv("DD_APP_KEY")
SITE = "https://api.datadoghq.com"

# Initialize LLMObs - ideally this should be done once at application/module startup
LLMObs.enable(
    ml_app="aegis",
    api_key=DD_API_KEY,
    site="datadoghq.com", # Default site, usually 
    agentless_enabled=True # Useful if no local agent
)

def emit_metrics(prompt, output, fw, gov, error=False):
    ts = int(time.time())

    tokens_in = len(prompt.split())
    tokens_out = len(output.split())
    cost = (tokens_in + tokens_out) * 0.000002  # mock $/token for demo

    # 1. Custom Metrics (Keep existing manual push if desired, or migrate to statsd)
    series = [
        {"metric": "aegis.llm.requests", "points": [[ts, 1]], "type": "count"},
        {"metric": "aegis.llm.errors", "points": [[ts, 1 if error else 0]], "type": "count"},
        {"metric": "aegis.llm.firewall.blocked", "points": [[ts, 1 if not fw["allowed"] else 0]], "type": "count"},
        {"metric": "aegis.llm.hallucination", "points": [[ts, gov.get("hallucination", 0.0)]]},
        {"metric": "aegis.llm.tokens_in", "points": [[ts, tokens_in]]},
        {"metric": "aegis.llm.tokens_out", "points": [[ts, tokens_out]]},
        {"metric": "aegis.llm.cost_usd", "points": [[ts, cost]]},
    ]

    try:
        requests.post(
            f"{SITE}/api/v1/series",
            headers={
                "DD-API-KEY": DD_API_KEY,
                "Content-Type": "application/json",
            },
            json={"series": series},
            timeout=3,
        )
    except Exception as e:
        print(f"Error sending metrics: {e}")

    # 2. LLM Observability Trace (Using SDK)
    try:
        # Start a trace for the LLM call
        with LLMObs.llm(
            model_name=os.environ.get("GEMINI_MODEL_NAME", "gemini-3-flash-preview"),
            model_provider="google",
            name="gemini_generate",
        ) as span:
            
            # Annotate input/output
            LLMObs.annotate(
                input_data=[{"role": "user", "content": prompt}],
                output_data=[{"role": "assistant", "content": output}],
                metrics={
                    "input_token_count": tokens_in,
                    "output_token_count": tokens_out,
                    "hallucination_score": gov.get("hallucination", 0),
                    "blocked": not fw["allowed"]
                },
                tags={
                    "env": "prod",
                    "version": "v1"
                }
            )
            
            if error:
                span.set_error(message="Inference failed")
                
    except Exception as e:
         print(f"Error sending LLM Trace: {e}")
