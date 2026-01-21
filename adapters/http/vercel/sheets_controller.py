from fastapi import APIRouter
from application.read_sheet_rows import (
    read_sheet_by_name,
    create_user_in_sheet
)
from application.models.excel_data import ExcelData
import os

router = APIRouter(
    prefix="/sheets",
    tags=["sheets"]
)


@router.get("/")
def get_sheet(table: str = "users"):
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")    

    if not SPREADSHEET_ID:
        raise RuntimeError("SPREADSHEET_ID not set")

    return read_sheet_by_name(SPREADSHEET_ID, table)

@router.post("/users")
def create_user_endpoint(data: ExcelData, table: str = "users"):
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

    if not SPREADSHEET_ID:
        raise RuntimeError("SPREADSHEET_ID not set")
    create_user_in_sheet(SPREADSHEET_ID, table, data)   
    return {"status": "created"}