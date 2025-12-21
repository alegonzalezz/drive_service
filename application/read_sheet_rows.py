from infrastructure.google.sheet_reader import read_first_rows, append_row
from application.models.excel_data import ExcelData


def read_sheet(sheet_id: str) -> list[dict]:
    """
    Caso de uso.
    No sabe nada de HTTP ni de frameworks.
    """
    return read_first_rows(sheet_id, limit=10)

def create_user(sheet_id: str, data: ExcelData):
    return append_row(sheet_id, data)
