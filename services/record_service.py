from bson import ObjectId
from fastapi import HTTPException, status
from database.connection import records_collection
from schemas.record import RecordCreate, RecordUpdate
from typing import Optional


def record_doc_to_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "amount": doc["amount"],
        "type": doc["type"],
        "category": doc["category"],
        "date": doc["date"],
        "description": doc.get("description"),
    }


async def create_record(data: RecordCreate) -> dict:
    record_doc = {
        "_id": str(ObjectId()),
        "amount": data.amount,
        "type": data.type.value,
        "category": data.category,
        "date": str(data.date),
        "description": data.description,
    }
    await records_collection.insert_one(record_doc)
    return record_doc_to_response(record_doc)


async def get_all_records(
    category: Optional[str] = None,
    type: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> list:
    query = {}

    if category:
        query["category"] = category
    if type:
        query["type"] = type

    # Date range filter
    if date_from or date_to:
        query["date"] = {}
        if date_from:
            query["date"]["$gte"] = date_from
        if date_to:
            query["date"]["$lte"] = date_to

    records = await records_collection.find(query).to_list(length=500)
    return [record_doc_to_response(r) for r in records]


async def get_record_by_id(record_id: str) -> dict:
    record = await records_collection.find_one({"_id": record_id})
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return record_doc_to_response(record)


async def update_record(record_id: str, data: RecordUpdate) -> dict:
    update_fields = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_fields:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    if "type" in update_fields:
        update_fields["type"] = update_fields["type"].value
    if "date" in update_fields:
        update_fields["date"] = str(update_fields["date"])

    result = await records_collection.update_one({"_id": record_id}, {"$set": update_fields})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    return await get_record_by_id(record_id)


async def delete_record(record_id: str) -> dict:
    result = await records_collection.delete_one({"_id": record_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return {"message": "Record deleted successfully"}
