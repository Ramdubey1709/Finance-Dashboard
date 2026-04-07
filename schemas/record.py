from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from models.record import RecordType


class RecordCreate(BaseModel):
    amount: float = Field(..., gt=0)
    type: RecordType
    category: str = Field(..., min_length=1)
    date: date
    description: Optional[str] = None


class RecordUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[RecordType] = None
    category: Optional[str] = None
    date: Optional[date] = None
    description: Optional[str] = None


class RecordResponse(BaseModel):
    id: str
    amount: float
    type: RecordType
    category: str
    date: str
    description: Optional[str] = None
