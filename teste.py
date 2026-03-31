import requests

headers = {
    "Autorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc1NTkyNTg3fQ.hp_ZnEC3gdHwSAflSMOq9sqIdW-pbbcsOVcIrhk70fA"
}

request = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(request)
print(request.json)