import urllib.request
import json
import time

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzcxOTIzMDg1fQ.pT92fFSSat0eqv1BIVud6b_pwK9LdUyV8TdRW-z3sX0"
BASE_URL = "http://127.0.0.1:8000/api/v1"

def make_request(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Content-Type", "application/json")
    
    if data:
        json_data = json.dumps(data).encode("utf-8")
        req.data = json_data
        
    try:
        with urllib.request.urlopen(req) as response:
            return response.getcode(), json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.read().decode()}")
        return e.code, None
    except Exception as e:
        print(f"Error: {e}")
        return 0, None

def verify():
    print("1. Checking Initial Stats...")
    code, stats = make_request("GET", "/incidents/stats")
    if code != 200:
        print(f"Failed to get stats. Code: {code}")
        if code == 404:
            print("User likely does not exist. You may need to create a user with ID 1.")
        return

    initial_threats = stats.get("active_threats", 0)
    print(f"Initial Active Threats: {initial_threats}")

    print("\n2. Injecting Web Attack (SQL Injection)...")
    payload = {
        "url": "http://example.com/login",
        "method": "POST",
        "user_agent": "Mozilla/5.0",
        "payload": "' OR 1=1 --",
        "ip": "1.2.3.4"
    }
    code, resp = make_request("POST", "/monitor/log/web", data=payload)
    if code == 201 or code == 200:
        print("Injection successful.")
    else:
        print(f"Injection failed. Code: {code}")
        return

    # Give DB a moment? Usually instant.
    time.sleep(1)

    print("\n3. Checking Stats Increment...")
    code, stats_new = make_request("GET", "/incidents/stats")
    if code != 200:
        print("Failed to get stats after injection.")
        return

    new_threats = stats_new.get("active_threats", 0)
    print(f"New Active Threats: {new_threats}")
    
    if new_threats > initial_threats:
        print("SUCCESS: Active threats increased!")
    else:
        print("FAILURE: Active threats did not increase.")

if __name__ == "__main__":
    verify()
