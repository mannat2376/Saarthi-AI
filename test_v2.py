import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_v2_flow():
    print("--- 🚀 Testing Saarthi AI V2 Flow ---")
    
    # 1. Trigger Emergency (Semantic Input)
    print("\n[Step 1] Triggering Emergency with chaotic input...")
    emergency_data = {
        "intent": "possible_cardiac_arrest",
        "confidence": 0.85,
        "symptoms": ["unresponsive", "breathing abnormal", "collapsed"],
        "speech_rate": 0.9,       # High stress
        "pause_irregularity": 0.8 # High stress
    }
    
    response = requests.post(f"{BASE_URL}/process", json=emergency_data)
    result = response.json()
    
    print(f"Current State: {result['current_state']}")
    print(f"UI Mode: {result['ui_mode']} (Expected RED)")
    print(f"Overload Score: {result['overload_analysis']['total_score']}")
    print(f"Needs Confirmation: {result['needs_confirmation']}")
    
    if result["needs_confirmation"]:
        print(f"\n[Step 2] Safety Step Detected: {result['instruction']}")
        input("Press Enter to simulate user clicking 'YES' button...")
        
        conf_response = requests.post(f"{BASE_URL}/confirm-step")
        print(f"Step Confirmed: {conf_response.json()['status']}")
        
        # Check next state
        status = requests.get(f"{BASE_URL}/status").json()
        print(f"New State: {status['current_state']} (Expected transition to RESPONSIVENESS)")
        print(f"Next Instruction: {status['instruction']}")

if __name__ == "__main__":
    try:
        test_v2_flow()
    except Exception as e:
        print(f"Error: {e}. Make sure 'python3 app.py' is running in another terminal.")
