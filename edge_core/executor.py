from enum import Enum
from typing import Dict, List, Optional
import time

class EmergencyState(Enum):
    IDLE = "IDLE"
    ASSESS_SAFETY = "ASSESS_SAFETY"
    CHECK_RESPONSIVENESS = "CHECK_RESPONSIVENESS"
    CALL_911 = "CALL_911"
    CHECK_PULSE = "CHECK_PULSE"
    CPR_ACTIVE = "CPR_ACTIVE"
    AED_GUIDANCE = "AED_GUIDANCE"
    RESOLVED = "RESOLVED"

class MedicalExecutor:
    def __init__(self):
        self.state = EmergencyState.IDLE
        self.start_time = None
        self.history: List[Dict] = []
        self.panic_level = 0
        self.logs = []
        self.step_confirmed = False  # Track if the current interactive step is confirmed

    def update(self, semantic_data: Dict, panic_score: int) -> Dict:
        """
        The deterministic brain. Takes semantic AI data (intent, symptoms) 
        and panic score, returns the NEXT step and UI instructions.
        """
        self.panic_level = panic_score
        intent = semantic_data.get("intent", "")
        symptoms = semantic_data.get("symptoms", [])
        
        # Determine UI Adaptation Level (Track 4.2)
        ui_adaptation = "GREEN"
        if panic_score > 3: ui_adaptation = "YELLOW"
        if panic_score > 5: ui_adaptation = "RED"  # HERO MODE

        # State Transition Logic (Deterministic + Interactive)
        if self.state == EmergencyState.IDLE:
            if intent == "possible_cardiac_arrest" or any(s in ["collapsed", "unresponsive"] for s in symptoms):
                self.state = EmergencyState.ASSESS_SAFETY
                self.start_time = time.time()
                self.step_confirmed = False

        elif self.state == EmergencyState.ASSESS_SAFETY:
            # Requires user to confirm "Safe" manually
            if self.step_confirmed:
                self.state = EmergencyState.CHECK_RESPONSIVENESS
                self.step_confirmed = False

        elif self.state == EmergencyState.CHECK_RESPONSIVENESS:
            if "unresponsive" in symptoms or intent == "unresponsive_patient":
                self.state = EmergencyState.CALL_911
                self.step_confirmed = False

        elif self.state == EmergencyState.CALL_911:
            # Requires user confirmation that call is placed
            if self.step_confirmed:
                self.state = EmergencyState.CHECK_PULSE
                self.step_confirmed = False

        elif self.state == EmergencyState.CHECK_PULSE:
            if "no pulse" in symptoms or "not breathing" in symptoms:
                self.state = EmergencyState.CPR_ACTIVE
                self.step_confirmed = False

        # Log the transition
        self.logs.append({
            "timestamp": time.time(),
            "state": self.state.value,
            "panic": panic_score,
            "intent": intent,
            "symptoms": symptoms
        })

        return {
            "current_state": self.state.value,
            "instruction": self._get_instruction(),
            "ui_mode": ui_adaptation,
            "is_emergency": self.state != EmergencyState.IDLE,
            "needs_confirmation": self._needs_confirmation()
        }

    def confirm_step(self):
        """Allows the UI to manually confirm a state-locked safety step."""
        self.step_confirmed = True
        
        # Proactively check for immediate transition
        if self.state == EmergencyState.ASSESS_SAFETY:
            self.state = EmergencyState.CHECK_RESPONSIVENESS
            self.step_confirmed = False
        elif self.state == EmergencyState.CALL_911:
            self.state = EmergencyState.CHECK_PULSE
            self.step_confirmed = False
            
        return {"status": "step_confirmed", "new_state": self.state.value}

    def _needs_confirmation(self) -> bool:
        """Returns True if the current state requires manual human confirmation."""
        return self.state in [EmergencyState.ASSESS_SAFETY, EmergencyState.CALL_911]

    def _get_instruction(self) -> str:
        """Returns the medically certified instructions for the current state."""
        instructions = {
            EmergencyState.IDLE: "Monitoring for cardiac emergencies...",
            EmergencyState.ASSESS_SAFETY: "IS THE ENVIRONMENT SAFE? Look for fire, traffic, or hazards. Tap 'YES' to confirm safety.",
            EmergencyState.CHECK_RESPONSIVENESS: "Tap their shoulders and shout 'Are you okay?'.",
            EmergencyState.CALL_911: "The patient is unresponsive. CALL 911 IMMEDIATELY. Tap 'CALLED' when done.",
            EmergencyState.CHECK_PULSE: "Check for pulse and breathing for 10 seconds. Place fingers on the side of the neck.",
            EmergencyState.CPR_ACTIVE: "START CPR. Push hard and fast in the center of the chest (100-120 bpm). I will keep the beat.",
            EmergencyState.AED_GUIDANCE: "AED is here. Turn it on and follow its voice commands immediately.",
            EmergencyState.RESOLVED: "First responders are here. Hand over the patient."
        }
        return instructions.get(self.state, "Keep following current steps.")

if __name__ == "__main__":
    # Small test loop
    executor = MedicalExecutor()
    print(executor.update("collapsed", 3))
    print(executor.update("safe", 5))
    print(executor.update("unresponsive", 9)) # Should trigger RED mode
