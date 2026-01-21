from infrastructure.google.get_sheets_service import get_sheets_service

def ensure_sheet_exists(spreadsheet_id: str, sheet_name: str) -> None:
    service = get_sheets_service()

    spreadsheet = service.spreadsheets().get(
        spreadsheetId=spreadsheet_id
    ).execute()

    sheets = spreadsheet.get("sheets", [])
    existing = [
        s["properties"]["title"] for s in sheets
    ]

    if sheet_name in existing:
        return

    # 1. Crear la hoja
    create_response = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": sheet_name,
                            "index": 0,
                            "gridProperties": {
                                "rowCount": 11,      # 1 header + 10 filas
                                "columnCount": 4     # A-D
                            }
                        }
                    }
                }
            ]
        }
    ).execute()

    sheet_id = create_response["replies"][0]["addSheet"]["properties"]["sheetId"]

    # 2. Escribir headers
    headers = [["id", "nombre", "edad", "email"]]

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A1:D1",
        valueInputOption="RAW",
        body={"values": headers}
    ).execute()

    # 3. Formato tipo “tabla”
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "requests": [
                # Header verde + bold
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": 0,
                            "endRowIndex": 1
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": {
                                    "red": 0.2,
                                    "green": 0.5,
                                    "blue": 0.4
                                },
                                "textFormat": {
                                    "bold": True,
                                    "foregroundColor": {
                                        "red": 0,
                                        "green": 0,
                                        "blue": 0
                                    }
                                }
                            }
                        },
                        "fields": "userEnteredFormat(backgroundColor,textFormat)"
                    }
                },

                # Filtro
                {
                    "setBasicFilter": {
                        "filter": {
                            "range": {
                                "sheetId": sheet_id,
                                "startRowIndex": 0,
                                "startColumnIndex": 0,
                                "endColumnIndex": 4
                            }
                        }
                    }
                },

                # Filas alternadas
                {
                    "addBanding": {
                        "bandedRange": {
                            "range": {
                                "sheetId": sheet_id,
                                "startRowIndex": 0,
                                "startColumnIndex": 0,
                                "endColumnIndex": 4
                            },
                            "rowProperties": {
                                "firstBandColor": {
                                    "red": 0.95,
                                    "green": 0.95,
                                    "blue": 0.95
                                },
                                "secondBandColor": {
                                    "red": 1,
                                    "green": 1,
                                    "blue": 1
                                }
                            }
                        }
                    }
                }
            ]
        }
    ).execute()

