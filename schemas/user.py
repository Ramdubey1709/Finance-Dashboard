from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from models.user import Role


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    role: Role = Role.viewer


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Role] = None


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: Role
    is_active: bool
