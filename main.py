from fastapi import FastAPI
from routers import users, records, dashboard

app = FastAPI(
    title="Finance Dashboard API",
    description="A backend API for managing financial records with role-based access control.",
    version="1.0.0",
)

app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)


@app.get("/", tags=["Health"])
async def root():
    return {"message": "Finance Dashboard API is running"}
