import requests
import json


def gen_token(username, password):
    url = "https://accept.paymob.com/api/auth/tokens"

    payload = json.dumps(
        {
            "username": username,
            "password": password
        }
    )
    headers = {"Content-Type": "application/json"}

    token = requests.request("POST", url, headers=headers, data=payload).json()

    return token
