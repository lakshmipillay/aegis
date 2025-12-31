
from fastapi import FastAPI, Body
from contextlib import asynccontextmanager
import vertexai
import logging
import os
from firewall import check_firewall
from governance import score_governance
from gemini import infer
from telemetry import emit_metrics
import prompt_manager

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
    # 1. Firewall Check
    fw = check_firewall(prompt)
    if not fw["allowed"]:
        emit_metrics(prompt, "BLOCKED", fw, {}, error=False)
        return {"text": "I cannot answer that."}

    # 2. Inference
    try:
        output = infer(prompt)
    except Exception as e:
        logger.error(f"Inference error: {e}")
        emit_metrics(prompt, "", fw, {}, error=True)
        return {"text": "Internal Error"}

    # 3. Governance Check
    gov = score_governance(output)

    # 4. Telemetry
    emit_metrics(prompt, output, fw, gov, error=False)

    return {"text": output}

@app.post("/webhook/patch")
def patch_endpoint(alert: dict = Body(...)):
    """
    Simulated Webhook from Datadog.
    Payload expected: {"attack_prompt": "...", "breach_response": "..."}
    """
    try:
        logger.info("Received Security Alert! Initiating Auto-Patch...")
        
        attack_prompt = alert.get("attack_prompt", "Unknown attack")
        
        # 1. Analyze Breach & Generate Fix using Vertex AI directly
        from vertexai.generative_models import GenerativeModel
        
        current_system = prompt_manager.get_system_prompt()
        model_name = os.environ.get("GEMINI_MODEL_NAME", "gemini-3-flash-preview")
        analyzer_model = GenerativeModel(model_name)
        analysis_prompt = f"""
        You are a Security Engineer.
        Our system prompt was LEAKED or bypassed by this attack: "{attack_prompt}".
        
        Current System Instructions:
        "{current_system}"
        
        Task: Write a NEW, IMPROVED system prompt that specifically blocks this attack type while maintaining the original persona.
        Return ONLY the new system prompt text.
        """
        
        resp = analyzer_model.generate_content(analysis_prompt)
        new_prompt = resp.text.strip()
        
        # 2. Apply Patch
        prompt_manager.update_system_prompt(new_prompt)
        
        logger.info("Auto-Patch Applied Successfully.")
        return {"status": "patched", "new_prompt": new_prompt}

    except Exception as e:
        import traceback
        error_msg = f"Webhook Failed: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        # Return 200 with error info so we can see it in trigger_patch.py output (instead of generic 500)
        return {"status": "error", "message": error_msg}
