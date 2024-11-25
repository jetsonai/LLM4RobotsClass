import requests
import json
 
url = 'http://127.0.0.1:8080/inference'
 
files = {
    'file': open('/home/nvidia/wav/goforward1.wav', 'rb'),
    'response-format': (None, 'json'),
}
 
response = requests.post(url, files=files)
result = json.loads(response.text)["text"]
print(result)
