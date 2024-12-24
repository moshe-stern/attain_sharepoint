import math
import os

import requests
from dotenv import load_dotenv
from pandas import DataFrame

if not load_dotenv():
    raise Exception("Failed to load .env")
headers = {
    "Accept": "application/json",
    "x-functions-key": os.getenv("FUNCTION_KEY"),
}
azure = os.getenv("FUNCTION_URL")
local = "http://localhost:7071"
base_url = local


def append(
    prefix: str,
    code: str,
    payload: list[dict[str, str | None]],
    row,
    email_arr: list[str],
):
    email = getattr(row, "Work_Email", "")
    if email not in email_arr:
        email = getattr(row, "Personal_Email", "")
    payload.append(
        {
            "employeeCode": f"{prefix}_{getattr(row, 'Employee_Code', "")}",
            "employeeNumber": getattr(row, code, ""),
            "position": getattr(row, "Position", ""),
            "workStatus": getattr(row, "DOL_Status", ""),
            "line1": getattr(row, "Street", ""),
            "line2": getattr(f" {row}, ", "Street Line 2", ""),
            "city": getattr(row, "City", ""),
            "addressState": getattr(row, "State", ""),
            "zipCode": str(getattr(row, "Zipcode", "")).zfill(5),
            "gender": getattr(row, "Gender", ""),
            "cellphone": getattr(row, "Primary_Phone", ""),
            "employeeStatus": getattr(row, "Employee_Status", ""),
            "metaDataS1": getattr(row, "SubRegionDesc", ""),
            "metaDataS2": "Migrated",
            "employeeEmail": email,
        }
    )
    for entry in payload:
        for key, value in entry.items():
            if isinstance(value, float) and math.isnan(value):
                entry[key] = None


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


def get_email_str():
    count: int = 0
    email_str: str = ""
    data = {"total": 1, "emails": ""}
    while count != data["total"]:
        data = medallion_api_get_emails(count)
        count += len(data["emails"].split(","))
        print(f"{count}/{data['total']}")
        email_str += data["emails"]
    return email_str


def update_providers(payload: list[dict[str, str | None]]):
    batch_size = 100
    success_count: list[bool] = []
    total_updated: int = 0
    total_payload = len(payload)
    updated_providers = []
    for count in range(0, total_payload, batch_size):
        current_payload = payload[count : count + batch_size]
        data = medallion_api_patch_providers(current_payload)
        success_count.extend(item["updated"] for item in data["updated"])
        total_updated += len(data["updated"])
        updated_providers.extend(data["updated"])
        print(f"Processed {total_updated}/{total_payload}")
    print(
        f"{success_count.count(True)}: updated, {success_count.count(False)}: failed to update"
    )
    return updated_providers


def validate_columns(required_fields: list[str], df: DataFrame):
    missing_columns = [col for col in required_fields if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
