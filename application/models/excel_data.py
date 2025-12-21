from pydantic import BaseModel
from typing import Optional


class ExcelData(BaseModel):
    id: int
    nombre: str
    edad: int
    email: Optional[str] = None
