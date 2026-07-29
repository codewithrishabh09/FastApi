from fastapi import FastAPI, HTTPException, Query, Path, Depends, Body
from app.services.employees import get_all_data, add_employee, remove_employee, update_employee_by_id
from app.schema.data_loader import Employee
from fastapi.responses import JSONResponse
from typing import List, Dict
import json
from datetime import datetime

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

@app.post("/Employee", status_code=201)
def Add_New_Employee(employee: Employee):
    employee_dict = employee.model_dump(mode="json")
    employee_dict["id"] = int()
    employee_dict["Added_Employee"] = datetime.utcnow().isoformat() + "z"

    try:
        save_employee = add_employee(employee_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"message": "Employee added sucessfully", "employee": save_employee}

@app.delete("/Employee/{employee_id}")
def deleted(employee_id: int = Path(..., ge=1, description="Employee ID to delete")):
    try:
        deleted = remove_employee(employee_id)
        return {"message": f"Employee {employee_id} Fired Successfully", "removed_employee": deleted}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
        
@app.put("/Employee/{employee_id}")
def update_full_employee(
    employee_id: int = Path(..., ge=1, description="Employee ID to update"),
    employee: Employee = Body(...)):
    try:
        employee_dict = employee.model_dump(mode="json")
        updated = update_employee_by_id(employee_id, employee_dict)
        return {"message": f"Employee {employee_id} updated Successfully", "updated_employee": updated}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    
