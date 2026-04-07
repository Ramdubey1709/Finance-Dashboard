from fastapi import APIRouter, Depends, Query, status
from schemas.record import RecordCreate, RecordUpdate, RecordResponse
from services import record_service
from utils.dependencies import require_role
from models.user import Role
from typing import List, Optional

router = APIRouter(prefix="/records", tags=["Financial Records"])

# Viewers, Analysts, and Admins can read records
read_access = require_role(Role.viewer, Role.analyst, Role.admin)

# Only Admins can create, update, delete
write_access = require_role(Role.admin)


@router.post("/", response_model=RecordResponse, status_code=status.HTTP_201_CREATED)
async def create_record(data: RecordCreate, _=Depends(write_access)):
    return await record_service.create_record(data)


@router.get("/", response_model=List[RecordResponse])
async def get_all_records(
    category: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None, description="Format: YYYY-MM-DD"),
    date_to: Optional[str] = Query(None, description="Format: YYYY-MM-DD"),
    _=Depends(read_access),
):
    return await record_service.get_all_records(category, type, date_from, date_to)


@router.get("/{record_id}", response_model=RecordResponse)
async def get_record(record_id: str, _=Depends(read_access)):
    return await record_service.get_record_by_id(record_id)


@router.put("/{record_id}", response_model=RecordResponse)
async def update_record(record_id: str, data: RecordUpdate, _=Depends(write_access)):
    return await record_service.update_record(record_id, data)


@router.delete("/{record_id}")
async def delete_record(record_id: str, _=Depends(write_access)):
    return await record_service.delete_record(record_id)
