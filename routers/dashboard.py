from fastapi import APIRouter, Depends
from services import dashboard_service
from utils.dependencies import require_role
from models.user import Role
from typing import List

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# Analysts and Admins can access dashboard
dashboard_access = require_role(Role.analyst, Role.admin)


@router.get("/summary")
async def get_summary(_=Depends(dashboard_access)):
    return await dashboard_service.get_dashboard_summary()


@router.get("/recent-transactions")
async def get_recent_transactions(_=Depends(dashboard_access)):
    return await dashboard_service.get_recent_transactions(limit=5)


@router.get("/monthly-summary")
async def get_monthly_summary(_=Depends(dashboard_access)):
    return await dashboard_service.get_monthly_summary()
