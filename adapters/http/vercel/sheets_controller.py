from fastapi import APIRouter
from application.read_sheet_rows import read_sheet, create_user
from application.models.excel_data import ExcelData
SPREADSHEET_ID = "1fPygn3Y1GgxKGUKi0ZTg_i_d-Ngv2lbQ45Foz1aK4kw"

router = APIRouter(
    prefix="/sheets",
    tags=["sheets"]
)


@router.get("/")
def get_sheet():
    return read_sheet(SPREADSHEET_ID)

@router.post("/users")
def create_user_endpoint(data: ExcelData):
    create_user(SPREADSHEET_ID, data)   
    return {"status": "created"}