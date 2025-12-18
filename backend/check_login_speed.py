import time
import requests

URL = "http://127.0.0.1:8000/api/v1/auth/login"
DATA = {"username": "admin@velvet.astro", "password": "admin"}

print(f"[*] Testing login speed for {URL}...")
start = time.time()
try:
    res = requests.post(URL, data=DATA)
    end = time.time()
    duration = end - start
    print(f"Status: {res.status_code}")
    print(f"Time: {duration:.4f} seconds")
    if res.status_code != 200:
        print(res.text)
except Exception as e:
    print(f"[-] Error: {e}")
