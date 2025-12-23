import requests

url = "http://127.0.0.1:8000/api/v1/auth/login"
payload = {
    "username": "admin@velvet.com",
    "password": "password"
}
try:
    print(f"Sending POST request to {url}...")
    response = requests.post(url, data=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
