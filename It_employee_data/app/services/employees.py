import json
from pathlib import Path
from typing import List, Dict

data_file = Path(__file__).resolve().parent.parent.parent / "data" / "test.json"

def load_data() -> List[Dict]:
    if not data_file.exists():
        raise FileNotFoundError(f"Product fil not fond at {data_file}")
    with open(data_file, "r", encoding="utf-8") as file:
        return json.load(file)

def get_all_data() -> List[Dict]:
    return load_data()

def save_employee_data(employee: List[Dict]) -> None:
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(employee,f, indent=2, ensure_ascii=False)

def add_employee(employee: Dict) -> Dict:
    employees = load_data()

    if any(e["email"].lower() == employee["email"].lower() for e in employees):
        raise ValueError(f"Employee with email '{employee['email']}' already exist.")

    if any(e["phone"] == employee["phone"] for e in employees):
        raise ValueError(f"Employee with phone '{employee['phone']}' already exist.")
        
    new_id = max([e["id"] for e in employees], default=0) + 1
    employee["id"] =  new_id
    employees.append(employee)
    save_employee_data(employees)
    return employee

def remove_employee(employee_id: int) -> Dict:
    employees = load_data()
    index = next((i for i, e in enumerate(employees) if e["id"] == employee_id), None)
    if index is None:
        raise ValueError(f"Employee with id {employee_id} not found")
    deleted = employees.pop(index)
    save_employee_data(employees)
    return deleted

def update_employee_by_id(employee_id: int, employee_data: Dict) -> Dict:
    employees = load_data()
    index = next((i for i, e in enumerate(employees) if e["id"] == employee_id), None)
    if index is None:
        raise ValueError(f"Employee with id {employee_id} not found")
    employee_data["id"] = employee_id
    employees[index] = employee_data
    save_employee_data(employees)
    return employee_data