from fastapi import APIRouter, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/customers", tags=["customers"])

class Customer(BaseModel):
    id: str
    name: str
    age: int
    gender: str
    riskProfile: str
    aum: int
    lastContact: str
    relevance: int

CUSTOMERS = [
    {"id": "1", "name": "Alice Smith", "age": 34, "gender": "female", "riskProfile": "low", "aum": 120000, "lastContact": "2025-07-10T14:30:00Z", "relevance": 98},
    {"id": "2", "name": "Bob Johnson", "age": 45, "gender": "male", "riskProfile": "medium", "aum": 250000, "lastContact": "2025-07-12T09:15:00Z", "relevance": 95},
    {"id": "3", "name": "Carol Lee", "age": 29, "gender": "female", "riskProfile": "high", "aum": 80000, "lastContact": "2025-07-15T16:45:00Z", "relevance": 92},
    {"id": "4", "name": "David Kim", "age": 52, "gender": "male", "riskProfile": "medium", "aum": 300000, "lastContact": "2025-07-13T11:00:00Z", "relevance": 90},
    {"id": "5", "name": "Eva Brown", "age": 41, "gender": "female", "riskProfile": "low", "aum": 175000, "lastContact": "2025-07-11T13:20:00Z", "relevance": 88},
    {"id": "6", "name": "Frank Green", "age": 38, "gender": "male", "riskProfile": "high", "aum": 95000, "lastContact": "2025-07-09T10:10:00Z", "relevance": 85},
    {"id": "7", "name": "Grace Hall", "age": 27, "gender": "female", "riskProfile": "medium", "aum": 60000, "lastContact": "2025-07-14T15:00:00Z", "relevance": 83},
    {"id": "8", "name": "Henry Young", "age": 50, "gender": "male", "riskProfile": "low", "aum": 220000, "lastContact": "2025-07-08T08:30:00Z", "relevance": 80},
    {"id": "9", "name": "Ivy King", "age": 36, "gender": "female", "riskProfile": "high", "aum": 105000, "lastContact": "2025-07-16T17:25:00Z", "relevance": 78},
    {"id": "10", "name": "Jackie Lin", "age": 31, "gender": "other", "riskProfile": "medium", "aum": 70000, "lastContact": "2025-07-10T12:00:00Z", "relevance": 75},
    {"id": "11", "name": "Kevin Scott", "age": 43, "gender": "male", "riskProfile": "high", "aum": 130000, "lastContact": "2025-07-13T14:40:00Z", "relevance": 72},
    {"id": "12", "name": "Laura Adams", "age": 39, "gender": "female", "riskProfile": "low", "aum": 160000, "lastContact": "2025-07-12T10:50:00Z", "relevance": 70},
    {"id": "13", "name": "Mike Baker", "age": 48, "gender": "male", "riskProfile": "medium", "aum": 210000, "lastContact": "2025-07-11T09:35:00Z", "relevance": 68},
    {"id": "14", "name": "Nina Perez", "age": 33, "gender": "female", "riskProfile": "high", "aum": 90000, "lastContact": "2025-07-15T18:10:00Z", "relevance": 65},
    {"id": "15", "name": "Oscar Reed", "age": 55, "gender": "male", "riskProfile": "low", "aum": 350000, "lastContact": "2025-07-07T07:45:00Z", "relevance": 62},
    {"id": "16", "name": "Paula Torres", "age": 40, "gender": "female", "riskProfile": "medium", "aum": 145000, "lastContact": "2025-07-14T16:30:00Z", "relevance": 60},
    {"id": "17", "name": "Quinn Evans", "age": 28, "gender": "other", "riskProfile": "high", "aum": 75000, "lastContact": "2025-07-09T11:55:00Z", "relevance": 58},
    {"id": "18", "name": "Ryan White", "age": 46, "gender": "male", "riskProfile": "medium", "aum": 195000, "lastContact": "2025-07-13T13:05:00Z", "relevance": 55},
    {"id": "19", "name": "Sara Black", "age": 35, "gender": "female", "riskProfile": "low", "aum": 110000, "lastContact": "2025-07-12T15:15:00Z", "relevance": 52},
    {"id": "20", "name": "Tommy Gray", "age": 42, "gender": "male", "riskProfile": "high", "aum": 125000, "lastContact": "2025-07-11T17:50:00Z", "relevance": 50},
]


# Pure function for filtering customers
def filter_customers(
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_dir: Optional[str] = "desc",
    gender: Optional[str] = None,
    riskProfile: Optional[str] = None,
    aum_min: Optional[int] = None,
    aum_max: Optional[int] = None,
    age_min: Optional[int] = None,
    age_max: Optional[int] = None,
):
    data = CUSTOMERS
    # Filter
    if gender:
        data = [c for c in data if c["gender"] == gender]
    if riskProfile:
        data = [c for c in data if c["riskProfile"] == riskProfile]
    if aum_min is not None:
        data = [c for c in data if c["aum"] >= int(aum_min)]
    if aum_max is not None:
        data = [c for c in data if c["aum"] <= int(aum_max)]
    if age_min is not None:
        data = [c for c in data if c["age"] >= int(age_min)]
    if age_max is not None:
        data = [c for c in data if c["age"] <= int(age_max)]
    # Search (by name)
    if search:
        data = [c for c in data if search.lower() in c["name"].lower()]
    # Sort
    if sort_by and sort_by in data[0]:
        reverse = sort_dir == "desc"
        data = sorted(data, key=lambda c: c[sort_by], reverse=reverse)
    return data

# API endpoint uses Query for docs, but passes plain values to filter_customers
@router.get("/", response_model=List[Customer])
def get_customers(
    search: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None),
    sort_dir: Optional[str] = Query("desc"),
    gender: Optional[str] = Query(None),
    riskProfile: Optional[str] = Query(None),
    aum_min: Optional[int] = Query(None),
    aum_max: Optional[int] = Query(None),
    age_min: Optional[int] = Query(None),
    age_max: Optional[int] = Query(None),
):
    return filter_customers(
        search=search,
        sort_by=sort_by,
        sort_dir=sort_dir,
        gender=gender,
        riskProfile=riskProfile,
        aum_min=aum_min,
        aum_max=aum_max,
        age_min=age_min,
        age_max=age_max,
    )
