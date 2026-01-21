from infrastructure.google.sheet_reader import (
    read_first_rows,
    append_row
)
from application.models.excel_data import ExcelData
from infrastructure.google.sheet_setup import ensure_sheet_exists



# -------- Casos de uso existentes --------

def read_sheet(sheet_id: str) -> list[dict]:
    return read_first_rows(sheet_id, limit=10)


def create_user(sheet_id: str, data: ExcelData):
    return append_row(sheet_id, data)


# -------- Nuevos casos de uso --------

def read_sheet_by_name(
    sheet_id: str,
    sheet_name: str,
    limit: int = 10
) -> list[dict]:
    """
    Caso de uso.
    Asegura la existencia de la hoja y luego la lee.
    """
    ensure_sheet_exists(
        spreadsheet_id=sheet_id,
        sheet_name=sheet_name
    )

    return read_first_rows(
        sheet_id=sheet_id,
        sheet_name=sheet_name,
        limit=limit
    )


def create_user_in_sheet(
    sheet_id: str,
    sheet_name: str,
    data: ExcelData
):
    """
    Caso de uso.
    Asegura la existencia de la hoja y luego inserta el registro.
    """
    ensure_sheet_exists(
        spreadsheet_id=sheet_id,
        sheet_name=sheet_name
    )

    return append_row(
        spreadsheet_id=sheet_id,
        sheet_name=sheet_name,
        data=data
    )
