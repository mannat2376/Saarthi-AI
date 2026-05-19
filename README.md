# Saarthi AI | Stress-Aware Emergency Response Edge Engine

A lightweight, on-device decision support system and state machine for emergency cardiac triage. It processes real-time voice feature metrics to estimate cognitive overload (stress) and dynamically adapts triage UI states and emergency routing logic.

## Core Pillars

1. **Lightweight Edge Classifier (MicroML)**: A NumPy-based logistic regression classifier executing feedforward inference to estimate cognitive overload based on speech rate and pause irregularity metrics.
2. **Deterministic Triage State Machine**: A robust medical state machine that coordinates transitions from assessment through safe responsive checks, 911 activation, and CPR pacing.
3. **Adaptive UX Control**: Implements panic-sensitive UI state transitions, escalating from `GREEN` (calm instructions) to `RED` (`HERO MODE` with minimized text, high-contrast indicators, and automated prompts) when high stress is predicted.
4. **Local Failure Logging**: Automatically logs triage events locally to enable asynchronous syncing when cellular or WiFi networks are absent.

---

## Technical Architecture

```
    Voice Input (Speech Rate, Pauses)
                 │
                 ▼
         NumPy Inference (MicroML)
                 │
                 ▼
       Cognitive Load Level
       - LOW   → UI: GREEN (Detailed instructions)
       - MED   → UI: YELLOW (Action prompts)
       - HIGH  → UI: RED (HERO MODE — simplified prompts)
                 │
                 ▼
     Medical State Machine (MedicalExecutor)
  [IDLE → ASSESS_SAFETY → CHECK_RESPONSIVENESS → CALL_911 → CPR]
                 │
                 ▼
   FastAPI Web Endpoint / Local Storage Sync
```

---

## Model Specification: MicroML (Logistic Regression)
- **Features Used**:
  - `speech_rate`: Speech frequency normalized between 0.0 and 1.0.
  - `pause_irregularity`: Silence intervals/stops normalized between 0.0 and 1.0.
  - `keyword_density`: Triage text complexity.
  - `repetition_score`: Lexical repetition patterns.
- **Inference Formula**:
  $$z = W \cdot X + b$$
  $$P(\text{overload}) = \sigma(z) = \frac{1}{1 + e^{-z}}$$
- **Execution Cost**: $< 0.1\text{ms}$ (100% on-device, NumPy only).

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Check service health and engine mode |
| `/process` | POST | Process semantic symptoms and calculate stress level |
| `/confirm-step` | POST | Manually confirm a state-locked triage step (e.g. environment safe, call placed) |
| `/status` | GET | Get current active state, panic level, and instruction |

---

## Setup & Running

### Dependencies
```bash
pip install -r requirements.txt
```

### Running the Engine
Start the FastAPI server:
```bash
python app.py
```

### Verification
Run the automated validation script to simulate low and high stress triage cases and verify engine responses:
```bash
python verify_engine.py
```
This generates a detailed validation report saved to `logs/verification_log.txt`.

## Project Structure
```
Saarthi-AI/
├── edge_core/
│   ├── executor.py         # Deterministic emergency state machine
│   ├── load_analyzer.py    # NumPy-based cognitive stress model
│   └── storage.py          # Local incident sync helper
├── logs/
│   └── verification_log.txt # Automated test report
├── app.py                  # FastAPI REST gateway
├── verify_engine.py        # Simulated triage integration tests
├── requirements.txt
└── README.md
```

## Contributors
- **Mannat Singh** — State Machine, NumPy Classifier, FastAPI Endpoints, Verification Framework
