import json

from fastapi import requests
import requests


def test_check_login():
    url = "http://127.0.0.1:8000/login"

    payload = {}
    headers = {
        'accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    assert response.status_code == 200
    json_response = json.loads(response.text)
    success = json_response["success"]
    print("status is " + str(success))
    assert success == True


def test_check_bank():
    url = "http://127.0.0.1:8000/login"

    payload = {}
    headers = {
        'accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    assert response.status_code == 200
    json_response = json.loads(response.text)
    bank = json_response["user"]["bank_data"][0]["bank_name"]
    print(bank)
    assert bank == "UK"
