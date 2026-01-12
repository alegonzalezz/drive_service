import csv
import requests
from io import StringIO
from application.models.excel_data import ExcelData
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os
import json

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "service-account.json"
range="users"

def get_sheets_service():
    service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    print(service_account_json) 
    if not service_account_json:
        creds = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES
        )
        return build("sheets", "v4", credentials=creds)
    else:
        service_account_info = json.loads(service_account_json)
        print("---------------------------")
        print(service_account_info)
        print("---------------------------")
        creds = Credentials.from_service_account_info(
            service_account_info,
            scopes=SCOPES
        )
        return build("sheets", "v4", credentials=creds)


def read_first_rows(sheet_id: str, limit: int = 10) -> list[dict]:
    """
    Infraestructura pura.
    Sabe cómo hablar con Google Sheets vía CSV.
    """

    service = get_sheets_service()
    rows = service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=range
    ).execute()
    
    values = rows.get("values", [])

    result = []
    for i, row in enumerate(values):
        if i > 0:
            print("_______________")
            print(row)
            print("_______________")
            result.append(
                ExcelData(
                    id=int(row[0]),
                    nombre=row[1],
                    edad=int(row[2]) if len(row) > 2 and row[2] != "" else None,
                    email=row[3] if len(row) > 3 else None
                )
            )

    return result



def append_row(spreadsheet_id: str, data: ExcelData):
    service = get_sheets_service()

    values = [[
        data.id,
        data.nombre,
        data.edad,
        data.email
    ]]

    body = {
        "values": values
    }

    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range,          # hoja Usuarios
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()
