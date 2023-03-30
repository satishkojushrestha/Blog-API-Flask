import requests

BASE = "http://127.0.0.1:5000/"

response = requests.post(BASE + "user/register", {"first-name":"Satish","last-name":"Shrestha","username":"satish123","password":"hellokcha"})
print(response.json())