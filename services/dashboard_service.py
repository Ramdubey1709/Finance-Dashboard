from database.connection import records_collection
from collections import defaultdict


async def get_dashboard_summary() -> dict:
    records = await records_collection.find().to_list(length=1000)

    total_income = 0.0
    total_expenses = 0.0
    category_totals = defaultdict(float)

    for r in records:
        amount = r["amount"]
        if r["type"] == "income":
            total_income += amount
        else:
            total_expenses += amount
        category_totals[r["category"]] += amount

    net_balance = total_income - total_expenses

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_balance": round(net_balance, 2),
        "category_totals": dict(category_totals),
    }


async def get_recent_transactions(limit: int = 5) -> list:
    # Sort by date descending, take last N
    records = await records_collection.find().sort("date", -1).limit(limit).to_list(length=limit)
    return [
        {
            "id": str(r["_id"]),
            "amount": r["amount"],
            "type": r["type"],
            "category": r["category"],
            "date": r["date"],
            "description": r.get("description"),
        }
        for r in records
    ]


async def get_monthly_summary() -> list:
    records = await records_collection.find().to_list(length=1000)

    # Group by year-month
    monthly = defaultdict(lambda: {"income": 0.0, "expenses": 0.0})

    for r in records:
        # date is stored as "YYYY-MM-DD"
        month_key = r["date"][:7]  # "YYYY-MM"
        if r["type"] == "income":
            monthly[month_key]["income"] += r["amount"]
        else:
            monthly[month_key]["expenses"] += r["amount"]

    result = []
    for month, totals in sorted(monthly.items()):
        result.append({
            "month": month,
            "income": round(totals["income"], 2),
            "expenses": round(totals["expenses"], 2),
            "net": round(totals["income"] - totals["expenses"], 2),
        })

    return result
