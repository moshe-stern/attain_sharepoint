import pandas as pd
from medallion.provider_updates.methods import get_email_str, validate_columns, append, update_providers
from share_point_csv import get_csv

required_fields = [
    "Employee_Code",
    "employee_number",
    "Position",
    "DOL_Status",
    "Street",
    "Street Line 2",
    "City",
    "State",
    "Zipcode",
    "Gender",
    "Primary_Phone",
    "Employee_Status",
    "SubRegionDesc",
    "Work_Email",
    "Personal_Email",
]


def medallion_provider_updates():
    updated_data_for_csv: list[dict[str, str | None]] = []
    email_str_arr = get_email_str().split(",")
    update_roster(
        email_str_arr,
        updated_data_for_csv,
        "kadiant",
        {"Sub-Region_-_CR_Desc": "SubRegionDesc", "ClockSeq_#": "ClockSeq"},
        "CRTeamMemberID",
        "KA",
    )
    update_roster(
        email_str_arr,
        updated_data_for_csv,
        "attain",
        {"ClockSeq_#": "ClockSeq", "Sub-Region_Desc": "SubRegionDesc"},
        "ClockSeq",
        "AT",
    )
    df = pd.DataFrame(updated_data_for_csv)
    csv_file_path = "../output.csv"
    df.to_csv(csv_file_path, index=False)


def update_roster(
    email_str_split: list[str],
    updated_data_for_csv: list[dict[str, str | None]],
    roster: str,
    cols: dict[str, str],
    id_field: str,
    id_prefix: str,
):
    payload: list[dict[str, str | None]] = []
    csv = get_csv(roster)
    df = pd.read_csv(csv)
    df = df.rename(columns=cols)
    df["Work_Email"] = df["Work_Email"].str.lower()
    df["Personal_Email"] = df["Personal_Email"].str.lower()
    required_fields[1] = id_field
    validate_columns(required_fields, df)
    filter_df = df[
        (df["Work_Email"].isin(email_str_split))
        | (df["Personal_Email"].isin(email_str_split))
    ]
    for row in filter_df.itertuples():
        append(id_prefix, id_field, payload, row, email_str_split)
    updated_data_for_csv.extend(update_providers(payload))