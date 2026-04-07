from bson import ObjectId
from fastapi import HTTPException, status
from database.connection import users_collection
from schemas.user import UserCreate, UserUpdate


def user_doc_to_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "email": doc["email"],
        "role": doc["role"],
        "is_active": doc["is_active"],
    }


async def create_user(data: UserCreate) -> dict:
    existing = await users_collection.find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user_doc = {
        "_id": str(ObjectId()),
        "name": data.name,
        "email": data.email,
        "role": data.role.value,
        "is_active": True,
    }
    await users_collection.insert_one(user_doc)
    return user_doc_to_response(user_doc)


async def get_all_users() -> list:
    users = await users_collection.find().to_list(length=100)
    return [user_doc_to_response(u) for u in users]


async def get_user_by_id(user_id: str) -> dict:
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_doc_to_response(user)


async def update_user(user_id: str, data: UserUpdate) -> dict:
    update_fields = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_fields:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    # Convert role enum to value if present
    if "role" in update_fields:
        update_fields["role"] = update_fields["role"].value

    result = await users_collection.update_one({"_id": user_id}, {"$set": update_fields})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return await get_user_by_id(user_id)


async def set_user_active_status(user_id: str, is_active: bool) -> dict:
    result = await users_collection.update_one({"_id": user_id}, {"$set": {"is_active": is_active}})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return await get_user_by_id(user_id)
