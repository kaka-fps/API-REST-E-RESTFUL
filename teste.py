import requests

headers = {
    "Autorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc1NjQ5NjU4fQ.DhQVqBjTf1auHWU0rULgPDEGKK6mYl7qi3UBGr9JwUw"
}

request = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(request)
print(request.json)