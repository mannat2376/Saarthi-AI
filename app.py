from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from edge_core.executor import MedicalExecutor
from edge_core.storage import IncidentStorage
from edge_core.load_analyzer import LoadAnalyzer
import uvicorn

app = FastAPI(title="Saarthi AI Edge Engine V2")

# Singleton instances
executor = MedicalExecutor()
storage = IncidentStorage()
analyzer = LoadAnalyzer()

class SemanticInput(BaseModel):
    intent: str
    confidence: float
    symptoms: List[str]
    # Mock speech metrics for the demo
    speech_rate: float = 0.5
    pause_irregularity: float = 0.5

@app.get("/")
def read_root():
    return {"status": "Saarthi AI Edge Engine V2 is running", "mode": "STRESS_AWARE_OFFLINE"}

@app.post("/process")
def process_emergency(user_input: SemanticInput):
    """
    V2 Process: Analyzes cognitive load and updates the medical state based on semantic AI output.
    """
    # 1. Analyze Cognitive Overload
    load_metrics = {
        "speech_rate": user_input.speech_rate,
        "pause_irregularity": user_input.pause_irregularity,
        # repetition and keyword density would be parsed from text in a full pipeline
        "keyword_density": 0.6 if len(user_input.symptoms) > 2 else 0.3 
    }
    load_result = analyzer.calculate_score(load_metrics)
    
    # 2. Update Medical Logic
    semantic_data = {
        "intent": user_input.intent,
        "symptoms": user_input.symptoms
    }
    panic_score = int(load_result["total_score"] * 10)
    
    result = executor.update(semantic_data, panic_score)
    result["overload_analysis"] = load_result
        
    if result["is_emergency"]:
        storage.log_incident(result)
        
    return result

@app.post("/confirm-step")
def confirm_step():
    """Manually unlock the next medical step (Feedback Loop)."""
    return executor.confirm_step()

@app.get("/status")
def get_current_status():
    return {
        "current_state": executor.state.value,
        "panic_level": executor.panic_level,
        "instruction": executor._get_instruction(),
        "needs_confirmation": executor._needs_confirmation()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
