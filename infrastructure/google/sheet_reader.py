from application.models.excel_data import ExcelData
from infrastructure.google.get_sheets_service import get_sheets_service

range="users"


def read_first_rows(sheet_id: str,sheet_name: str, limit: int = 10) -> list[dict]:
    """
    Infraestructura pura.
    Sabe cómo hablar con Google Sheets vía CSV.
    """

    service = get_sheets_service()
    rows = service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=f"{sheet_name}"
    ).execute()
    
    values = rows.get("values", [])

    result = []
    for i, row in enumerate(values):
        if i > 0:
            result.append(
                ExcelData(
                    id=int(row[0]),
                    nombre=row[1],
                    edad=int(row[2]) if len(row) > 2 and row[2] != "" else None,
                    email=row[3] if len(row) > 3 else None
                )
            )

    return result



def append_row(spreadsheet_id: str, sheet_name: str, data: ExcelData):
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
        range=f"{sheet_name}",          # hoja Usuarios
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()


