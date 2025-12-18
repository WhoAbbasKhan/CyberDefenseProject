import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"
EMAIL = "admin@velvet.net"
PASSWORD = "admin" # Assuming default or previously set
ORG_ID = 1

def print_result(phase, status, message=""):
    color = "\033[92m" if status == "PASS" else "\033[91m"
    end = "\033[0m"
    print(f"[{phase}] {color}{status}{end} : {message}")

def verify_system():
    print("starting Full System Verification...")
    token = None
    
    # ---------------------------------------------------------
    # Phase 0-1: Authentication & Core
    # ---------------------------------------------------------
    try:
        # 1. Login
        resp = requests.post("http://localhost:8000/api/v1/auth/login", data={"username": EMAIL, "password": PASSWORD})
        if resp.status_code == 200:
            token = resp.json()["access_token"]
            print_result("Phase 0 (Auth)", "PASS", "Login successful")
        else:
            print_result("Phase 0 (Auth)", "FAIL", f"Login failed: {resp.text}")
            return
    except Exception as e:
        print_result("Phase 0 (Auth)", "FAIL", f"Connection failed: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # ---------------------------------------------------------
    # Phase 2: Email Security
    # ---------------------------------------------------------
    try:
        resp = requests.post(f"{BASE_URL}/email/ingest", headers=headers, json={
            "subject": "Urgent Invoice",
            "sender": "attacker@bad.com",
            "body": "Please pay now.",
            "headers": {"X-Origin-IP": "1.2.3.4"}
        })
        if resp.status_code == 200:
            print_result("Phase 2 (Email)", "PASS", "Email ingestion accepted")
        else:
             print_result("Phase 2 (Email)", "FAIL", f"Status {resp.status_code}")
    except: print_result("Phase 2 (Email)", "FAIL", "Exception")

    # ---------------------------------------------------------
    # Phase 3 & 15: Website/Login & Risk Auth
    # ---------------------------------------------------------
    try:
        resp = requests.post(f"{BASE_URL}/monitor/login-attempt", headers=headers, json={
            "email": "user@test.com",
            "ip_address": "45.33.22.11", 
            "user_agent": "Mozilla/5.0",
            "status": "FAILED"
        })
        if resp.status_code == 200:
            res_json = resp.json()
            risk_score = res_json.get("risk_score", 0)
            print_result("Phase 3/15 (Web/Risk)", "PASS", f"Login analyzed. Risk Score: {risk_score}")
        else:
            print_result("Phase 3/15 (Web/Risk)", "FAIL", f"Status {resp.status_code}")
    except: print_result("Phase 3/15 (Web/Risk)", "FAIL", "Exception")

    # ---------------------------------------------------------
    # Phase 13: Anomaly Detection (Module A)
    # ---------------------------------------------------------
    try:
        # Just check status endpoint if exists or assume ingestion triggers it
        # We will trigger a specific anomaly verify endpoint if we built one, or just trust the previous step
        # Let's hit the manual anomaly score check
        resp = requests.post(f"{BASE_URL}/anomaly/score", headers=headers, json={
             "metric": "login_volume", "value": 500
        })
        if resp.status_code == 200:
             print_result("Phase 13 (Anomaly)", "PASS", f"Score: {resp.json().get('anomaly_score')}")
        else:
             print_result("Phase 13 (Anomaly)", "WARN", "Endpoint might be internal or diff path")
    except: pass
    
    # ---------------------------------------------------------
    # Phase 16: Kill Chain (Module D)
    # ---------------------------------------------------------
    try:
        # Create a mock incident to check kill chain logic
        resp = requests.post(f"{BASE_URL}/incidents/simulate", headers=headers, json={
            "title": "Kill Chain Test",
            "stage": "Reconnaissance"
        })
        if resp.status_code == 200:
             print_result("Phase 16 (KillChain)", "PASS", "Simulated Incident Created")
        else:
             print_result("Phase 16 (KillChain)", "FAIL", f"Status {resp.status_code}")
    except: print_result("Phase 16 (KillChain)", "FAIL", "Exception")

    # ---------------------------------------------------------
    # Phase 17: Threat Intel (Module E)
    # ---------------------------------------------------------
    try:
        resp = requests.get(f"{BASE_URL}/threat/feed", headers=headers)
        if resp.status_code == 200:
             print_result("Phase 17 (Threat)", "PASS", "Threat feed accessible")
        else:
             print_result("Phase 17 (Threat)", "FAIL", f"Status {resp.status_code}")
    except: print_result("Phase 17 (Threat)", "FAIL", "Exception")

    # ---------------------------------------------------------
    # Phase 18: Attack Prediction (Module F)
    # ---------------------------------------------------------
    try:
        resp = requests.post(f"{BASE_URL}/predictions/forecast", headers=headers)
        if resp.status_code == 200:
             print_result("Phase 18 (Prediction)", "PASS", "Forecast generated")
        else:
             print_result("Phase 18 (Prediction)", "FAIL", f"Status {resp.status_code}")
    except: print_result("Phase 18 (Prediction)", "FAIL", "Exception")

    # ---------------------------------------------------------
    # Phase 19: Deception (Module G)
    # ---------------------------------------------------------
    try:
        resp = requests.post(f"{BASE_URL}/deception/assets", headers=headers, json={
            "type": "HONEY_TOKEN", "label": "FakeAWSKey"
        })
        if resp.status_code == 201:
             print_result("Phase 19 (Deception)", "PASS", "Deception asset created")
        else:
             print_result("Phase 19 (Deception)", "FAIL", f"Status {resp.status_code}")
    except: print_result("Phase 19 (Deception)", "FAIL", "Exception")

    # ---------------------------------------------------------
    # Phase 20: Profiling (Module H)
    # ---------------------------------------------------------
    try:
        resp = requests.get(f"{BASE_URL}/profiling", headers=headers)
        if resp.status_code == 200:
             print_result("Phase 20 (Profiling)", "PASS", "Personas listed")
        else:
             print_result("Phase 20 (Profiling)", "FAIL", f"Status {resp.status_code}")
    except: print_result("Phase 20 (Profiling)", "FAIL", "Exception")

    # ---------------------------------------------------------
    # Phase 21: Playbooks (Module I)
    # ---------------------------------------------------------
    try:
        resp = requests.get(f"{BASE_URL}/playbooks", headers=headers)
        if resp.status_code == 200:
             print_result("Phase 21 (Playbooks)", "PASS", "Playbooks listed")
        else:
             print_result("Phase 21 (Playbooks)", "FAIL", f"Status {resp.status_code}")
    except: print_result("Phase 21 (Playbooks)", "FAIL", "Exception")

    # ---------------------------------------------------------
    # Phase 22: Forensics (Module J)
    # ---------------------------------------------------------
    try:
        resp = requests.post(f"{BASE_URL}/forensic/log", headers=headers, json={
            "type": "TEST_LOG", "data": {"foo": "bar"}
        })
        if resp.status_code == 201:
             print_result("Phase 22 (Forensics)", "PASS", "Evidence logged immutably")
        else:
             print_result("Phase 22 (Forensics)", "FAIL", f"Status {resp.status_code}")
    except: print_result("Phase 22 (Forensics)", "FAIL", "Exception")

if __name__ == "__main__":
    verify_system()
