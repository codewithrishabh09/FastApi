from fastapi import FastAPI, HTTPException, Query, Path, Depends
from app.services.employees import get_all_data
from fastapi.responses import JSONResponse
from typing import List, Dict
import json

app = FastAPI()
def common_logic():
    return "hello coder"

@app.get("/", response_model=dict)
def root(dep=Depends(common_logic)):
    return JSONResponse(
        status_code=200,
        content={
            "message": "welcome to Employee Endpoit",
            "dependency": dep
        },
    )

@app.get("/Employees", response_model=Dict)
def Employee_List(name: str = Query(
    default=None,
    min_length=3,
    max_length=20,
    descripition="Serach by employee name.",
    example="Aditi Patel",
    ),

    sort_by_salary:bool = Query(
        default=False,
        descripition="Sort emoloyees by salary",
    ),
    order: str = Query(
        default="asc",
        descripition="Sort oder when sort_by_salary is used (asc/desc)",
    ),
    department: str = Query(
        default=None,
        descripition="Filter by department",
        example="Software Engineer",
    ),

    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        descripition="Number of items to return",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        descripition="Pagination offset",
    ),
):
     
    employees = get_all_data()
    
    if name:
        needle = name.strip().lower()
        employees = [
            e for e in employees
            if needle in f"{e['first_name']} {e['last_name']}".lower()
        ]

    if department:
        employees = [e for e in employees if e["department"].lower() == department.lower()]
    
    if not employees:
        raise HTTPException(status_code=404, detail=f"No employees found !")

    if sort_by_salary:
        reverse = order == "desc"
        employees = sorted(employees, key=lambda e: e["salary"], reverse=reverse)
    
    total = len(employees)
    employees = employees[offset: offset + limit]
    return{
        "total": total,
        "employees": employees
    }
    
@app.get("/Employees/{employee_id}", response_model=Dict)
def Get_Employees_By_ID(employee_id: int = Path(..., ge=1, description="Employee ID")):
    employees = get_all_data()
    employee = next((e for e in employees if e["id"] == employee_id), None)
    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee with id {employee_id} not found")
    return employee