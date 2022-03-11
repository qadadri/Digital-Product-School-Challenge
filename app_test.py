import requests


response = requests.post("http://10.188.199.121:5000/api/predict", headers={"Content-Type": "application/json"},
                         json={"year": "2021", "month": "-1"})

print(response.text)