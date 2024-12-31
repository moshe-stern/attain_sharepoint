from medallion.api import medallion_api_create_enrollments
from share_point_csv import get_csv
import pandas as pd

def create_payor_enrollments():
    df = pd.read_csv('./Payer Address Mapping(Sheet1).csv')
    enrollments: list[dict[str, str]] = []
    df = df[df['State'] == 'CA']
    for row in df.itertuples():
        enrollments.append({
            'ServiceAddress': getattr(row, 'Service_Address', ''),
            'Payor': getattr(row, "Payor", ''),
            'Entity': getattr(row, 'Entity', ''),
            'Payor Type': getattr(row, 'Payor')
        })
    res = medallion_api_create_enrollments({
        'enrollments': enrollments,
        'state': 'CA'
    })
    print(res)

