import urllib.request
import urllib.parse
import json

URL = "http://127.0.0.1:8000/api/v1/auth/login"
DATA = {
    "username": "admin@velvet.com",
    "password": "password"
}

def login():
    data = urllib.parse.urlencode(DATA).encode()
    req = urllib.request.Request(URL, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    
    try:
        with urllib.request.urlopen(req) as res:
            print(f"Status: {res.status}")
            print(res.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error: {e.code}")
        print(e.read().decode())
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    login()
