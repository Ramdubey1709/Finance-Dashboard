# Finance Dashboard API

A backend REST API built with FastAPI and MongoDB for managing financial records with role-based access control.

**Live API:** https://finance-dashboard-iiac.onrender.com  
**Interactive Docs (Swagger UI):** https://finance-dashboard-iiac.onrender.com/docs  
**GitHub Repository:** https://github.com/Ramdubey1709/Finance-Dashboard

## Tech Stack

- Python 3.10+
- FastAPI
- MongoDB
- Motor (async MongoDB driver)
- Pydantic v2
- Uvicorn

## Project Structure

```
finance-dashboard/
├── main.py                  # App entry point
├── .env                     # Environment variables
├── requirements.txt
├── database/
│   └── connection.py        # MongoDB connection
├── models/
│   ├── user.py              # Role enum
│   └── record.py            # RecordType enum
├── schemas/
│   ├── user.py              # Pydantic schemas for users
│   └── record.py            # Pydantic schemas for records
├── routers/
│   ├── users.py             # User endpoints
│   ├── records.py           # Financial record endpoints
│   └── dashboard.py         # Dashboard/aggregation endpoints
├── services/
│   ├── user_service.py      # User business logic
│   ├── record_service.py    # Record business logic
│   └── dashboard_service.py # Aggregation logic
└── utils/
    └── dependencies.py      # RBAC dependencies
```

## Setup & Run

1. Make sure MongoDB is running locally on port 27017.

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Update `.env` with your MongoDB connection string.

4. Start the server:
```bash
uvicorn main:app --reload
```

5. Open the interactive docs at: http://localhost:8000/docs

---

## Authentication

This API uses a simple header-based user identification for demonstration purposes.

Pass the user's ID in every request header:
```
X-User-Id: <your_user_id>
```

> In a production app, this would be replaced with JWT token authentication.

---

## Roles & Permissions

| Role     | Users API | Records API | Dashboard API |
|----------|-----------|-------------|---------------|
| Viewer   | No        | GET only    | No            |
| Analyst  | No        | GET only    | Yes           |
| Admin    | Full      | Full        | Yes           |

---

## API Overview

### Users (Admin only)

| Method | Endpoint                        | Description          |
|--------|---------------------------------|----------------------|
| POST   | /users/                         | Create a user        |
| GET    | /users/                         | Get all users        |
| GET    | /users/{user_id}                | Get user by ID       |
| PUT    | /users/{user_id}                | Update user          |
| PATCH  | /users/{user_id}/activate       | Activate user        |
| PATCH  | /users/{user_id}/deactivate     | Deactivate user      |

### Financial Records

| Method | Endpoint                | Description                        |
|--------|-------------------------|------------------------------------|
| POST   | /records/               | Create a record (Admin)            |
| GET    | /records/               | Get all records with filters       |
| GET    | /records/{record_id}    | Get record by ID                   |
| PUT    | /records/{record_id}    | Update a record (Admin)            |
| DELETE | /records/{record_id}    | Delete a record (Admin)            |

Filtering query params for GET /records/:
- `category` — filter by category name
- `type` — `income` or `expense`
- `date_from` — start date (YYYY-MM-DD)
- `date_to` — end date (YYYY-MM-DD)

### Dashboard (Analyst + Admin)

| Method | Endpoint                       | Description                        |
|--------|--------------------------------|------------------------------------|
| GET    | /dashboard/summary             | Total income, expenses, net balance, category totals |
| GET    | /dashboard/recent-transactions | Last 5 transactions                |
| GET    | /dashboard/monthly-summary     | Income/expenses grouped by month   |

---

## Assumptions & Design Decisions

- Authentication is simulated via a `X-User-Id` request header. In a real system, this would be replaced with JWT-based auth. This approach was chosen to keep the focus on RBAC and API design rather than auth infrastructure.
- User IDs are stored as strings (using MongoDB ObjectId converted to string) for simplicity and readability.
- Financial record dates are stored as `YYYY-MM-DD` strings. This keeps date range filtering simple and readable without requiring date serialization complexity.
- The `Analyst` role can read records and access all dashboard summaries, but cannot create, update, or delete records. Only `Admin` has full write access.
- The `Viewer` role can only read financial records — no dashboard access, no write access.
- There is no self-registration endpoint. Users are created by an Admin. The first Admin must be seeded directly into the database (a `seed.py` script is provided for this).
- Soft delete is not implemented. Delete is permanent. This is a known tradeoff for simplicity.
- No pagination is implemented. Record listing returns up to 500 records, which is acceptable for an assignment scope.

## Tradeoffs

- Chose Motor (async MongoDB driver) over PyMongo to align with FastAPI's async nature, giving better performance under concurrent requests.
- Kept aggregation logic in Python (in-memory grouping) rather than MongoDB aggregation pipelines. This is simpler to read and understand, which fits the assignment's emphasis on clarity over optimization.
- Header-based auth instead of JWT keeps the codebase focused on the actual requirements without adding auth boilerplate.

---

## Example Usage

### 1. Create an Admin user (no auth needed for first user — use MongoDB directly or seed)

You can insert a user directly into MongoDB to bootstrap:
```json
{
  "_id": "admin-001",
  "name": "Alice",
  "email": "alice@example.com",
  "role": "Admin",
  "is_active": true
}
```

### 2. Create a financial record
```bash
curl -X POST http://localhost:8000/records/ \
  -H "Content-Type: application/json" \
  -H "X-User-Id: admin-001" \
  -d '{"amount": 5000, "type": "income", "category": "Salary", "date": "2024-01-15"}'
```

### 3. Get dashboard summary
```bash
curl http://localhost:8000/dashboard/summary \
  -H "X-User-Id: admin-001"
```

### 4. Filter records by type and date range
```bash
curl "http://localhost:8000/records/?type=expense&date_from=2024-01-01&date_to=2024-01-31" \
  -H "X-User-Id: admin-001"
```
