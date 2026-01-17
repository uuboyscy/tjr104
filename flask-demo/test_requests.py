import requests

res = requests.get("http://10.2.19.139:5001/api/recommendation/allen001")
print(res.json())