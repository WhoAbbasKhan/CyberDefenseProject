import requests
import sys

BASE_URL = "http://127.0.0.1:8000/api/v1"
EMAIL = "admin@velvet.astro"
PASSWORD = "admin"

def verify():
    # 1. Login
    print(f"[*] Logging in as {EMAIL}...")
    try:
        res = requests.post(f"{BASE_URL}/auth/login", data={"username": EMAIL, "password": PASSWORD})
        res.raise_for_status()
        token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("[+] Login Successful")
    except Exception as e:
        print(f"[-] Login Failed: {e}")
        return

    # 2. Check Live Attacks (Web Events)
    print("\n[*] Verifying /monitor/events (Live Attacks)...")
    try:
        res = requests.get(f"{BASE_URL}/monitor/events", headers=headers)
        if res.status_code == 200:
            events = res.json()
            print(f"[+] Success: Retrieved {len(events)} events")
        else:
            print(f"[-] Failed: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[-] Error: {e}")

    # 3. Check Defense Rules
    print("\n[*] Verifying /defense/rules...")
    try:
        # Create Rule
        rule_data = {
            "name": "Test Rule Python",
            "if_type": "SQL Injection",
            "if_severity": "Critical",
            "then_action": "Block IP",
            "is_active": True
        }
        res_create = requests.post(f"{BASE_URL}/defense/rules", json=rule_data, headers=headers)
        if res_create.status_code == 200:
             print("[+] Created Test Rule")
             rule_id = res_create.json()["id"]
             
             # List Rules
             res_list = requests.get(f"{BASE_URL}/defense/rules", headers=headers)
             print(f"[+] Loaded {len(res_list.json())} rules")
             
             # Delete Rule
             requests.delete(f"{BASE_URL}/defense/rules/{rule_id}", headers=headers)
             print("[+] Deleted Test Rule")
        else:
             print(f"[-] Failed to create rule: {res_create.status_code} - {res_create.text}")

    except Exception as e:
         print(f"[-] Error: {e}")

    # 4. Check Training
    print("\n[*] Verifying /training/me...")
    try:
        res = requests.get(f"{BASE_URL}/training/me", headers=headers)
        if res.status_code == 200:
            print(f"[+] Success: Retrieved {len(res.json())} training assignments")
        else:
            print(f"[-] Failed: {res.status_code} - {res.text}")

        # Trigger Demo
        print("[*] Triggering Demo Training...")
        res_trig = requests.post(f"{BASE_URL}/training/trigger", json={"email": EMAIL, "trigger_type": "phishing_click"}, headers=headers)
        if res_trig.status_code == 200:
             print("[+] Triggered Training Assignment")
             # Check again
             res_me = requests.get(f"{BASE_URL}/training/me", headers=headers)
             print(f"[+] Updated Assignments: {len(res_me.json())}")
        else:
             print(f"[-] Trigger Failed: {res_trig.status_code} - {res_trig.text}")

    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    verify()
