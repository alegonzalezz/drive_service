import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "service-account.json"
range="users"

def get_sheets_service():
    service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not service_account_json:
        creds = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES
        )
        return build("sheets", "v4", credentials=creds)
    else:
        service_account_info = json.loads(service_account_json)
        creds = Credentials.from_service_account_info(
            service_account_info,
            scopes=SCOPES
        )
        return build("sheets", "v4", credentials=creds)