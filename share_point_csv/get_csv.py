import os
from io import BytesIO
import requests
from dotenv import load_dotenv

if not load_dotenv():
    raise Exception("Failed to load .env")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
tenant_id = os.getenv("TENANT_ID")
sharepoint_domain_name = os.getenv("SHARE_POINT_DOMAIN_NAME")
resource = f"{os.getenv('RESOURCE')}/{sharepoint_domain_name}@{tenant_id}"

file_path = f"/sites/bi/Shared Documents/Power Automate/FOR DIGACORE"
sites= {
    'bi':'bi',
    'billing': 'billing'
}
file_urls = {
    "attain": file_path + "/Attain TSS - Roster Files/Attain TSS - Roster Files.csv",
    "kadiant": file_path
    + "/Kadiant - Roster Files/Team Member Kadiant Roster IT Combined.csv",
}


def get_csv(roster: str, site: str):
    headers = {"Authorization": f"Bearer {get_access_token()}", "Accept": "*/*"}
    file_url = f"https://{sharepoint_domain_name}/sites/{sites[site]}/_api/web/GetFileByServerRelativeUrl('{file_urls[roster]}')/$value"
    file_response = requests.get(file_url, headers=headers)
    if file_response.status_code != 200:
        raise Exception("Failed to retrieve file:", file_response.text)
    file_content = BytesIO(file_response.content)
    return file_content


def get_access_token():
    token_url = f"https://accounts.accesscontrol.windows.net/{tenant_id}/tokens/OAuth/2"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "resource": "00000003-0000-0ff1-ce00-000000000000/attainaba.sharepoint.com@d82742c9-4dd4-4162-a3ef-7727c0d9d588",
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception("Failed to retrieve access token:", response.text)
