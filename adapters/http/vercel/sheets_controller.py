from fastapi import APIRouter
from application.read_sheet_rows import read_sheet, create_user
from application.models.excel_data import ExcelData
import os

router = APIRouter(
    prefix="/sheets",
    tags=["sheets"]
)


@router.get("/")
def get_sheet():
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

    if not SPREADSHEET_ID:
        raise RuntimeError("SPREADSHEET_ID not set")

    return read_sheet(SPREADSHEET_ID)

@router.post("/users")
def create_user_endpoint(data: ExcelData):
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

    if not SPREADSHEET_ID:
        raise RuntimeError("SPREADSHEET_ID not set")
    create_user(SPREADSHEET_ID, data)   
    return {"status": "created"}