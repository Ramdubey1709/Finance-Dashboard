"""
Run this script once to insert test data into MongoDB.
Usage: python seed.py
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "finance_dashboard"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# ── Test Users ──────────────────────────────────────────────────────────────
users = [
    {
        "_id": "admin-001",
        "name": "Alice Admin",
        "email": "alice@example.com",
        "role": "Admin",
        "is_active": True,
    },
    {
        "_id": "analyst-001",
        "name": "Bob Analyst",
        "email": "bob@example.com",
        "role": "Analyst",
        "is_active": True,
    },
    {
        "_id": "viewer-001",
        "name": "Charlie Viewer",
        "email": "charlie@example.com",
        "role": "Viewer",
        "is_active": True,
    },
    {
        "_id": "inactive-001",
        "name": "Dave Inactive",
        "email": "dave@example.com",
        "role": "Viewer",
        "is_active": False,
    },
]

# ── Test Financial Records ───────────────────────────────────────────────────
records = [
    {"_id": "rec-001", "amount": 50000.0, "type": "income",  "category": "Salary",      "date": "2024-01-15", "description": "January salary"},
    {"_id": "rec-002", "amount": 1200.0,  "type": "expense", "category": "Rent",        "date": "2024-01-20", "description": "Monthly rent"},
    {"_id": "rec-003", "amount": 300.0,   "type": "expense", "category": "Groceries",   "date": "2024-01-22", "description": "Weekly groceries"},
    {"_id": "rec-004", "amount": 50000.0, "type": "income",  "category": "Salary",      "date": "2024-02-15", "description": "February salary"},
    {"_id": "rec-005", "amount": 1200.0,  "type": "expense", "category": "Rent",        "date": "2024-02-20", "description": "Monthly rent"},
    {"_id": "rec-006", "amount": 5000.0,  "type": "income",  "category": "Freelance",   "date": "2024-02-25", "description": "Web project payment"},
    {"_id": "rec-007", "amount": 800.0,   "type": "expense", "category": "Utilities",   "date": "2024-02-28", "description": "Electricity + internet"},
    {"_id": "rec-008", "amount": 50000.0, "type": "income",  "category": "Salary",      "date": "2024-03-15", "description": "March salary"},
    {"_id": "rec-009", "amount": 2500.0,  "type": "expense", "category": "Travel",      "date": "2024-03-10", "description": "Flight tickets"},
    {"_id": "rec-010", "amount": 450.0,   "type": "expense", "category": "Groceries",   "date": "2024-03-18", "description": "Monthly groceries"},
    {"_id": "rec-011", "amount": 3000.0,  "type": "income",  "category": "Freelance",   "date": "2024-03-28", "description": "Logo design project"},
    {"_id": "rec-012", "amount": 1200.0,  "type": "expense", "category": "Rent",        "date": "2024-03-20", "description": "Monthly rent"},
]


async def seed():
    # Clear existing data
    await db["users"].delete_many({})
    await db["records"].delete_many({})

    # Insert fresh data
    await db["users"].insert_many(users)
    await db["records"].insert_many(records)

    print("✅ Seed complete!")
    print(f"   Inserted {len(users)} users")
    print(f"   Inserted {len(records)} financial records")
    print()
    print("Test user IDs to use as X-User-Id header:")
    print("   admin-001    → Admin (full access)")
    print("   analyst-001  → Analyst (read + dashboard)")
    print("   viewer-001   → Viewer (read only)")
    print("   inactive-001 → Inactive (should get 403)")

    client.close()


asyncio.run(seed())
