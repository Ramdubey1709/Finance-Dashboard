from fastapi import APIRouter, Depends, status
from schemas.user import UserCreate, UserUpdate, UserResponse
from services import user_service
from utils.dependencies import get_current_user, require_role
from models.user import Role
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

# Only Admins can manage users
admin_only = require_role(Role.admin)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, _=Depends(admin_only)):
    return await user_service.create_user(data)


@router.get("/", response_model=List[UserResponse])
async def get_all_users(_=Depends(admin_only)):
    return await user_service.get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, _=Depends(admin_only)):
    return await user_service.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, data: UserUpdate, _=Depends(admin_only)):
    return await user_service.update_user(user_id, data)


@router.patch("/{user_id}/activate", response_model=UserResponse)
async def activate_user(user_id: str, _=Depends(admin_only)):
    return await user_service.set_user_active_status(user_id, True)


@router.patch("/{user_id}/deactivate", response_model=UserResponse)
async def deactivate_user(user_id: str, _=Depends(admin_only)):
    return await user_service.set_user_active_status(user_id, False)
