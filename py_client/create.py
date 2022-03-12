import requests
from getpass import getpass


auth_endpoint = "http://127.0.0.1:8000/api/auth/"
username = input("Enter your username: ")
password = getpass("Enter your password: ")

auth_response = requests.post(
    auth_endpoint, json={'username': username, 'password': password})
print(auth_response.json())

if auth_response.status_code == 200:
    token = auth_response.json()['token']
    headers = {
        "Authorization": f"Token {token}"
    }

    endpoint = "http://127.0.0.1:8000/api/products/"

    data = {
        "title": "Hello",
        "content": "Helloo",
        "price": 49.99
    }

    get_response = requests.post(endpoint, headers=headers, json=data)

    print(get_response.json())
