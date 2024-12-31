import os
import requests
from dotenv import load_dotenv
if not load_dotenv():
    raise Exception("Failed to load .env")
headers = {
    "Accept": "application/json",
    "x-functions-key": os.getenv("FUNCTION_KEY"),
}
azure = os.getenv("FUNCTION_URL")
local = "http://localhost:7071"
base_url = local

def medallion_api_get_emails(offset: int):
    response = requests.get(
        f"{base_url}/api/providers/?email-string=true&offset={offset}",
        headers=headers,
    )
    if not response.ok:
        raise Exception(response.text)
    return response.json()


def medallion_api_patch_providers(data: list[dict[str, str]]):
    response = requests.patch(
        f"{base_url}/api/providers",
        headers={
            **headers,
            "Content-Type": "application/json",
        },
        json=data,
    )
    if not response.ok:
        raise Exception(response.text)
    return response.json()

def medallion_api_get_payor_list():
    pass

def medallion_api_create_enrollments(data):
    response = requests.post(
        f"{base_url}/api/payer-enrollments",
        headers={
            **headers,
            "Content-Type": "application/json",
        },
        json=data,
    )
    if not response.ok:
        raise Exception(response.text)
    return response.json()