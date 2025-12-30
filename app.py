
from fastapi import FastAPI, Body
from contextlib import asynccontextmanager
import vertexai
import logging
import os
from firewall import check_firewall
from governance import score_governance
from gemini import infer
from telemetry import emit_metrics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aegis")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Vertex AI
    try:
        project_id = "aegis-482716"
        location = "us-central1"
        logger.info(f"Initializing Vertex AI for project {project_id} in {location}...")
        vertexai.init(project=project_id, location=location)
        logger.info("Vertex AI initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Vertex AI: {e}")
        # We generally don't want to crash here so the container can start and log the error
    
    yield
    # Shutdown logic if needed

app = FastAPI(lifespan=lifespan)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Aegis is running"}

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
