import requests

BASE = "http://127.0.0.1:5000/"

#user registration
# response = requests.post(BASE + "user/register", {"first_name":"Satish","last_name":"Shrestha","username":"satish123","password":"test123"})
#user login
# response = requests.post(BASE + "login", {"username":"satish123","password":"test123"})

post_response = requests.get(BASE + "admin/post")
print(post_response.json())