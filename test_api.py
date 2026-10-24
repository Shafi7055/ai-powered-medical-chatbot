import requests, json
url = 'http://127.0.0.1:8000/api/chat'
payload = {"message": "What causes headaches?", "history": []}
try:
    r = requests.post(url, json=payload, timeout=10)
    print('Status:', r.status_code)
    print('Text:', r.text)
    print('JSON:', r.json())
except Exception as e:
    print('Error:', e)
