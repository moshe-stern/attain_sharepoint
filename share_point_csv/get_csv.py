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

file_path_bi = f"/sites/bi/Shared Documents/Power Automate/FOR DIGACORE"
payer_address_mapping = "/sites/billing/Shared%20Documents/Contracts%20&%20Fee%20Schedules/Payer%20Specific/Address%20Mapping/Payer%20Address%20Mapping.xlsx"
attain_roster = '/sites/bi/Shared%20Documents/Power%20Automate/FOR%20DIGACORE/Attain%20TSS%20-%20Roster%20Files/Team%20Member%20TSS%20Roster%20IT%20Combined.csv'
kadiant_roster = '/sites/bi/Shared%20Documents/Power%20Automate/FOR%20DIGACORE/Kadiant - Roster Files/Team Member Kadiant Roster IT Combined.csv'
sharepoint_file_urls = {
    "attain": attain_roster,
    "kadiant": kadiant_roster,
    'payer_address_mapping': payer_address_mapping
}


def get_csv(file: str):
    headers = {"Authorization": f"Bearer {get_access_token()}", "Accept": "*/*"}
    file_url = f"https://{sharepoint_domain_name}/{sharepoint_file_urls[file]}/_api/web/GetFileByServerRelativeUrl('{file}')/$value"
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
        "resource": f"{resource}/{sharepoint_domain_name}@{tenant_id}",
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception("Failed to retrieve access token:", response.text)
