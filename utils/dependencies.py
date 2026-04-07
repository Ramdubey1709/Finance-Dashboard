from fastapi import Header, HTTPException, status, Depends
from database.connection import users_collection
from models.user import Role


async def get_current_user(x_user_id: str = Header(..., description="Pass the user ID in the X-User-Id header")):
    """
    Simple auth simulation: client passes their user ID via header.
    In a real app, this would be a JWT token.
    """
    user = await users_collection.find_one({"_id": x_user_id})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not user.get("is_active", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive")
    return user


def require_role(*allowed_roles: Role):
    """Returns a dependency that checks if the current user has one of the allowed roles."""
    async def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in [r.value for r in allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[r.value for r in allowed_roles]}"
            )
        return current_user
    return role_checker
